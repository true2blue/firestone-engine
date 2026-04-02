setx FR_DB firestone-test
set FR_DB=firestone-test
@REM mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/init.js"
@REM mongo 127.0.0.1/firestone-test "c:/aqua/firestone-engine/tests/import_mocktrades.js"
@REM mongoimport -d firestone-data -c 600026-2026-04-02 --host 127.0.0.1:27018 --file "\tests\data\20260402\firestone-data.600026-2026-04-02.trades.json" --type json --jsonArray --drop
@REM mongoimport -d firestone-data -c 600798-2026-04-02 --host 127.0.0.1:27018 --file "\tests\data\20260402\firestone-data.600798-2026-04-02.trades.json" --type json --jsonArray --drop
@REM mongoimport -d firestone-data -c 601872-2026-04-02 --host 127.0.0.1:27018 --file "\tests\data\20260402\firestone-data.601872-2026-04-02.trades.json" --type json --jsonArray --drop
@REM mongoimport -d firestone-data -c 601919-2026-04-02 --host 127.0.0.1:27018 --file "\tests\data\20260402\firestone-data.601919-2026-04-02.trades.json" --type json --jsonArray --drop
@REM mongoimport -d firestone-data -c 601975-2026-04-02 --host 127.0.0.1:27018 --file "\tests\data\20260402\firestone-data.601975-2026-04-02.trades.json" --type json --jsonArray --drop
@REM mongo 127.0.0.1:27018/firestone-data --eval "db.getCollection('300448-2019-12-10').drop(); db.getCollection('399006-2019-12-10').drop(); db.getCollection('000993-2019-12-10').drop(); db.getCollection('000001-2019-12-10').drop();" "c:/aqua/firestone-engine/tests/e2e/batchydls/data.js"
REM mongoimport -d firestone-test -c codes "tests\concept\codes.json"
REM mongoimport -d firestone-test -c concepts "tests\concept\concepts.json"
REM mongoimport -d firestone-test -c hot_concept "tests\concept\hot_concept.json"
REM mongo 127.0.0.1/firestone-test "C:/aqua/firestone-engine/tests/concept/new_hot_concept.js"
REM mongo 127.0.0.1:27018/firestone-data --eval "db.dropDatabase(); db.getSiblingDB('firestone-data');"
REM mongo 127.0.0.1:27018/firestone-data "c:/aqua/firestone-engine/tests/initData.js"
REM mongo 127.0.0.1:27018/firestone-data "c:/aqua/firestone-engine/tests/strategies/ydls.js"
@REM mongoimport -d firestone-data -c 399006-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\399006-2024-01-08.json" --type "json"
@REM mongoimport -d firestone-data -c 399006-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\399006-2024-01-08.json" --type "json"
REM mongoimport -d firestone-data -c 000001-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\000001-2024-01-08.json" --type "json"
@REM mongoimport -d firestone-data -c 000993-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\000993-2024-01-08.json" --type "json"
REM mongoimport -d firestone-data -c 300693-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\300693-2024-01-08.json" --type "json"
REM mongoimport -d firestone-data -c 300691-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\300691-2024-01-08.json" --type "json"
REM pipenv run python -m unittest tests/strategies/TestBasic.py
REM pipenv run python -m unittest tests/strategies/TestBasicSell.py
REM pipenv run python -m unittest tests/strategies/TestYdls.py
REM pipenv run python -m unittest tests/TestMock.py
REM pipenv run python -m unittest tests/TestDataloader.py
REM pipenv run python -m unittest tests/strategies/TestConceptPick.py
pipenv run python -m unittest tests/strategies/TestBatchYdls.py
@REM pipenv run python -m unittest tests/strategies/TestFreeK.py
REM pipenv run python -m unittest tests/strategies/TestPPT0New.py
REM pipenv run python -m unittest tests/strategies/TestMultiBuy.py