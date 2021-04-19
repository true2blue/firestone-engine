import requests
import logging
import json

class ProxyManager(object):

    _URL = 'http://http.tiqu.alicdns.com/getip3?num={}&type=2&pro=&city=0&yys=100017&port=1&time=3&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'

    _LOAD_PROXY_RETRY = 10
    
    _logger = logging.getLogger(__name__)

    def __init__(self):
        self.proxy_pool = []
        self.load_proxy_failed = 0
        self.i = 0

    def load_proxies(self, number=5):
        try:
            response = requests.get(ProxyManager._URL.format(number))
            ProxyManager._logger.info('load proxies, retry = {} get response = {}'.format(self.load_proxy_failed, response.text))
            result = json.loads(response.text)
            if(result['code'] == 0):
                for data in result['data']:
                    self.proxy_pool.append(f'http://{data["ip"]}:{data["port"]}')
            else:
                ProxyManager._logger.error('get proxy failed code = {}'.format(result['code']))
                self.load_proxy_failed += 1
        except Exception as e:
            ProxyManager._logger.error('get proxy failed, e = {}'.format(e))
            self.load_proxy_failed += 1


    def get_pool_size(self):
        return len(self.proxy_pool)


    def get_proxy(self):
        if(self.get_pool_size() == 0):
            if(self.load_proxy_failed < ProxyManager._LOAD_PROXY_RETRY):
                self.load_proxies()
            if(self.get_pool_size() == 0):
                return None
        if self.i >= self.get_pool_size():
            self.i = 0
        proxy = self.proxy_pool[self.i]
        self.i = self.i + 1
        return proxy


    def remove_proxy(self, proxy):
        self.proxy_pool.remove(proxy)