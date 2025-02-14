setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/e2e/batchydls/init.js"
mongo 127.0.0.1:27018/firestone-data --eval "db.getCollection('300448-2019-12-10').drop(); db.getCollection('399006-2019-12-10').drop(); db.getCollection('000993-2019-12-10').drop(); db.getCollection('sh-2019-12-10').drop();" "c:/aqua/firestone-engine/tests/e2e/batchydls/data.js"
mongo 127.0.0.1:27018/firestone-data --eval "db.getCollection('300448-2019-12-10-m').drop(); db.getCollection('399006-2019-12-10-m').drop();db.getCollection('000993-2019-12-10-m').drop(); db.getCollection('sh-2019-12-10-m').drop();"
start dist\calculate.exe 5db7e0a555609bb27252edb8 --date 2019-12-10-m --hours * --minutes * -m -v -i -t
REM pipenv run firerock 5db7e0a555609bb27252edb8 --date 2019-12-10-m --hours * --minutes * -m -v -i -t -d
timeout /t 30
start dist\main.exe 300448 000993 399006 sh --date 2019-12-10 --hours * --minutes * -m -v
timeout /t 900 /nobreak > nul
pipenv run python -m unittest tests/e2e/batchydls/CheckBatchYdls.py