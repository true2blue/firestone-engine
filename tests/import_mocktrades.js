// import_mocktrades.js
// Reads a JSON array file and inserts into the mocktrades collection in 'firestone-test'.
// Designed to be run with the mongo shell on Windows.

var filePath = "c:/aqua/firestone-engine/tests/data/20260402/firestone.trades.json";
try {
    var content = cat(filePath);
    var arr = JSON.parse(content);
    var targetDb = db.getSiblingDB('firestone-test');
    targetDb.mocktrades.drop();
    if (Array.isArray(arr) && arr.length > 0) {
        // Convert MongoDB Extended JSON (e.g. {"$oid": "..."}, {"$date": "..."}) into real BSON types
        function convertExtendedJSON(value) {
            if (value === null || value === undefined) return value;
            if (Array.isArray(value)) {
                return value.map(convertExtendedJSON);
            }
            if (typeof value === 'object') {
                var keys = Object.keys(value);
                // Exact single-key extended JSON objects
                if (keys.length === 1) {
                    if (value.hasOwnProperty('$oid')) {
                        try { return ObjectId(value['$oid']); } catch (e) { return value; }
                    }
                    if (value.hasOwnProperty('$date')) {
                        var d = value['$date'];
                        if (typeof d === 'string') {
                            try { return ISODate(d); } catch (e) { return new Date(d); }
                        }
                        if (typeof d === 'object' && d.hasOwnProperty('$numberLong')) {
                            try { return new Date(parseInt(d['$numberLong'])); } catch (e) { return value; }
                        }
                    }
                }
                // Recurse into object properties
                var out = {};
                for (var k in value) {
                    if (value.hasOwnProperty(k)) {
                        out[k] = convertExtendedJSON(value[k]);
                    }
                }
                return out;
            }
            return value;
        }

        var converted = arr.map(convertExtendedJSON);
        try {
            // Use unordered insert so a duplicate _id or other write error doesn't abort the whole batch.
            var res = targetDb.mocktrades.insertMany(converted, { ordered: false });
            print('Inserted documents result: ' + tojson(res));
        } catch (e) {
            // BulkWriteError may occur (duplicate _id etc). Print summary and continue.
            print('Bulk insert finished with errors: ' + tojson(e));
            if (e.writeErrors && e.writeErrors.length) {
                print('Write errors: ' + e.writeErrors.length);
            }
            if (e.insertedIds) {
                try { print('Inserted ids count: ' + Object.keys(e.insertedIds).length); } catch (ie) {}
            }
        }
    } else {
        print('No documents found in ' + filePath);
    }
} catch (e) {
    print('Failed to import mocktrades from ' + filePath + ': ' + e);
    throw e;
}
