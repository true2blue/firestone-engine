setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/init.js"
mongoimport -d firestone-test -c codes "tests\concept\codes.json"
mongoimport -d firestone-test -c concepts "tests\concept\concepts.json"
mongoimport -d firestone-test -c hot_concept "tests\concept\hot_concept.json"
mongo 127.0.0.1/firestone-test "C:/aqua/firestone-engine/tests/concept/new_hot_concept.js"
mongo 127.0.0.1:27018/firestone-data --eval "db.dropDatabase(); db.getSiblingDB('firestone-data');"
mongo 127.0.0.1:27018/firestone-data "c:/aqua/firestone-engine/tests/initData.js"
mongo 127.0.0.1:27018/firestone-data "c:/aqua/firestone-engine/tests/strategies/ydls.js"
mongoimport -d firestone-data -c 399006-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\399006-2024-01-08.json" --type "json"
mongoimport -d firestone-data -c 000001-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\000001-2024-01-08.json" --type "json"
mongoimport -d firestone-data -c 000993-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\000993-2024-01-08.json" --type "json"
mongoimport -d firestone-data -c 300693-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\300693-2024-01-08.json" --type "json"
mongoimport -d firestone-data -c 300691-2024-01-08 --host 127.0.0.1:27018 --file "tests\data\300691-2024-01-08.json" --type "json"
REM pipenv run python -m unittest tests/strategies/TestBasic.py
REM pipenv run python -m unittest tests/strategies/TestBasicSell.py
REM pipenv run python -m unittest tests/strategies/TestYdls.py
REM pipenv run python -m unittest tests/TestMock.py
REM pipenv run python -m unittest tests/TestDataloader.py
REM pipenv run python -m unittest tests/strategies/TestConceptPick.py
REM pipenv run python -m unittest tests/strategies/TestBatchYdls.py
pipenv run python -m unittest tests/strategies/TestPPT0New.py