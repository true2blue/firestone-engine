import logging
import browser_cookie3
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import os

class CookieManager(object):

    _MONFO_URL = '127.0.0.1'

    _logger = logging.getLogger(__name__)
    
    def __init__(self):
        self.client = MongoClient(CookieManager._MONFO_URL, 27017)
        self.db = self.client[os.environ['FR_DB']]
        trigger = IntervalTrigger(minutes=2)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.run,trigger=trigger)
        self.count = 0

    def run(self):
        self.count += 1
        CookieManager._logger.info('Get cookie')
        # cj = browser_cookie3.chrome(domain_name='github.com')
        # cookie_str = ''
        # for cookie in cj:
        #     cookie_str += f"{cookie.name}={cookie.value}; "
        # print(cookie_str)
        configs = self.db['configs'].find({})
        for config in configs:
            print(config)
            self.db['configs'].update_one({"_id" : config['_id']},{"$set" : {'cookie' : self.count}})
        CookieManager._logger.info('Cookie updated successfully')

    def start(self):
        self.scheduler.start()
        CookieManager._logger.info('Cookie Schedule is started')

    def stop(self):
        self.scheduler.shutdown(wait=False)
        CookieManager._logger.info('Cookie Schedule is shutdown')

if __name__ == '__main__':
    manager = CookieManager()
    manager.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        manager.scheduler.shutdown()
        print("Scheduler has been shut down.")