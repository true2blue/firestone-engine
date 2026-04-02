from pymongo import MongoClient
from firestone_engine.strategies.BatchYdls import BatchYdls
from bson import ObjectId
import unittest

class TestBatchYdls(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['firestone-test']
        self.data_client = MongoClient('127.0.0.1', 27018)
        self.db_data = self.data_client['firestone-data']
        self.config = self.db['configmocks'].find_one({"_id" : ObjectId('69cd20ed9f6564554cca683c')})
        self.trade = self.db['mocktrades'].find_one({"_id" : ObjectId('69cd20ed9f6564554cca683c')})
        self.userId = '5d905db9fc84d3224b0eb59c'
        self.by = BatchYdls()
        self.load_data()


    def load_data(self):
        self.data = {
            '600026' : list(self.db_data['600026-2026-04-02'].find()),
            '600798' : list(self.db_data['600798-2026-04-02'].find()),
            '601872' : list(self.db_data['601872-2026-04-02'].find()),
            '601919' : list(self.db_data['601919-2026-04-02'].find()),
            '601975' : list(self.db_data['601975-2026-04-02'].find()),
        }
        self.index = {
            '000001' : list(self.db_data['000001-2026-04-02'].find()),
            '399006' : list(self.db_data['399006-2026-04-02'].find())
        }


    def test_batch_ydls(self):
        data = {
            '600026' : [],
            '600798' : [],
            '601872' : [],
            '601919' : [],
            '601975' : []
        }
        index = {
            '000001' : [],
            '399006' : []
        }
        for i in range(4479):
            if i < len(self.data['600026']):
                data['600026'].append(self.data['600026'][i])
            if i < len(self.data['600798']):
                data['600798'].append(self.data['600798'][i])
            if i < len(self.data['601872']):
                data['601872'].append(self.data['601872'][i])
            if i < len(self.data['601919']):
                data['601919'].append(self.data['601919'][i])
            if i < len(self.data['601975']):
                data['601975'].append(self.data['601975'][i])
            if i < len(self.index['000001']):
                index['000001'].append(self.index['000001'][i])
            if i < len(self.index['399006']):
                index['399006'].append(self.index['399006'][i])
            if(self.by.run(self.trade, self.config, self.db, data, index)):
                break
        self.assertEqual(data['600026'][-1]['time'], '09:38:39')


    def tearDown(self):
        self.client.close()


if __name__ == "__main__":
    unittest.main()

# to debug in vscode uncomment this block
import ptvsd
# 5678 is the default attach port in the VS Code debug configurations
print("start debug on port 5678")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()