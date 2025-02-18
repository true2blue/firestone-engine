import browser_cookie3
from pymongo import MongoClient
import os

class CookieManager(object):

    _MONFO_URL = '127.0.0.1'

    def __init__(self):
        self.client = MongoClient(CookieManager._MONFO_URL, 27017)
        self.db = self.client[os.environ['FR_DB']]

    def run(self):
        cj = browser_cookie3.firefox(domain_name='jy.xzsec.com')
        cookie_str = ''
        for cookie in cj:
            cookie_str += f"{cookie.name}={cookie.value}; "
        configs = self.db['configs'].find({})
        for config in configs:
            self.db['configs'].update_one({"_id" : config['_id']},{"$set" : {'cookie' : cookie_str}})

if __name__ == '__main__':
    manager = CookieManager()
    manager.run()