setx FR_DB firestone-test
mongo 127.0.0.1/firestone-test --eval "db.dropDatabase(); db.getSiblingDB('firestone-test');" "c:/aqua/firestone-engine/tests/init.js"
mongo 127.0.0.1:27018/firestone-data --eval "db.getCollection('300448-2019-12-10').drop(); db.getCollection('cyb-2019-12-10').drop();" "c:/aqua/firestone-engine/tests/e2e/ppt0/data.js"
mongo 127.0.0.1:27018/firestone-data --eval "db.getCollection('300448-2019-12-10-m').drop(); db.getCollection('cyb-2019-12-10-m').drop();"
start dist\main.exe 300448 cyb --date 2019-12-10 --hours * --minutes * -m -v
start "" pipenv run firerock 5db7e0a555609bb27252edb9 --date 2019-12-10-m --hours * --minutes * -m -v -i -t -d
timeout /t 900 /nobreak > nul
pipenv run python -m unittest tests/e2e/ppt0/CheckPPT0.py