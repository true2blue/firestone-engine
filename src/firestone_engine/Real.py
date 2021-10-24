from pymongo import MongoClient
from bson.objectid import ObjectId
from pydoc import locate
from datetime import datetime
from time import time
import os
import logging
from .Constants import Constants
from .strategies.Base import Base
from .strategies.Basic import Basic
from .strategies.Ydls import Ydls
from .strategies.BasicSell import BasicSell
from .strategies.ConceptPick import ConceptPick
from .strategies.BatchYdls import BatchYdls
from .strategies.PPT0 import PPT0
import requests
import json

class Real(object):

    _MONFO_URL = '127.0.0.1'

    _DATA_DB = 'firestone-data'

    _logger = logging.getLogger(__name__)

    def __init__(self, tradeId, date=None):
        self.tradeId = tradeId
        if(date is None):
            today = datetime.now()
            date = '{}-{}-{}'.format(today.year,('0' + str(today.month))[-2:],('0' + str(today.day))[-2:])
        self.date = date
        self.lastRunTime = None
        self.client = MongoClient(Real._MONFO_URL, 27017)
        self.db = self.client[os.environ['FR_DB']]
        self.data_client = MongoClient(Real._MONFO_URL, 27018)
        self.data_db = self.data_client[Real._DATA_DB]
        self.init_cols()
        self.init_Config()


    def init_cols(self):
        self.cols = {
            'trades' : 'trades',
            'configs' : 'configs'
        }   
        self.init_session()
        
    
    def init_session(self):
        self.__header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'jy.xzsec.com',
            'Origin': 'https://jy.xzsec.com',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }


    def run(self):
        self.load_trade_config()
        if(self.config['curBuyNum'] >= self.config['maxBuyNum'] and (not self.is_T0())):
            force_state = {'state' : Constants.STATE[4]}
            self.updateTrade(force_state)
            return force_state
        if(self.trade['state'] == Constants.STATE[5]):
            return self.cancelOrder()
        if(self.trade['state'] == Constants.STATE[0] and 'order' in self.trade and 'result' in self.trade['order']):
            htbh = self.trade['order']['result']['data']['htbh']
            self.updateTrade({'order' : {}})
            return {'state' : self.trade['state'], 'htbh' : htbh}
        if(self.trade['state'] == Constants.STATE[6] and 'order' in self.trade):
            htbh = ''
            if 'Wtbh' in self.trade['order']:
                htbh = self.trade['order']['Wtbh']
            elif 'd_2135' in self.trade['order']:
                htbh = self.trade['order']['d_2135']
            return {'state' : self.trade['state'], 'htbh' : htbh}
        if(self.trade['state'] != Constants.STATE[0] and self.trade['state'] != Constants.STATE[6]):
            return {'state' : self.trade['state']}
        if(self.strategy.need_create_order()):
            if(self.trade['result'] is not None and self.trade['result'] != '无' and self.trade['result'] != '' and self.trade['state'] != Constants.STATE[6]):
                self.updateTrade({'result' : '无'})
            self.load_data()
            if(len(self.data['data']) == 0):
                return {'state' : self.trade['state']}
            if(not self.is_batch()):
                if(self.data['data'][-1]['time'] == self.lastRunTime):
                    return {'state' : self.trade['state']}
                self.lastRunTime = self.data['data'][-1]['time']
            flag = False
            if(self.is_batch()):
                flag = self.strategy.run(self.trade, self.config, self.db, self.data['data'], self.data['index'])
            else:
                flag = self.strategy.run(self.trade, self.config, self.data['data'], self.data['index'])
            if(flag):
                result = self.createOrder()
                if(result['state'] == Constants.STATE[2]):
                    return {'state' : result['state'], 'htbh' : result['order']['result']['data']['htbh']}
        else:
            self.strategy.run(self.trade, self.config, self.db, type(self).__name__ == 'Mock')
        return {'state' : self.trade['state']}
    
    
    def get_op(self):
        return self.strategy.op if self.is_T0() else self.strategyMeta['op']


    
    def load_trade(self):
        self.trade = self.db[self.cols['trades']].find_one({"_id" : ObjectId(self.tradeId)})
    
    def load_trade_config(self):
        self.load_trade()
        self.config = self.db[self.cols['configs']].find_one({"userId" : self.trade['userId']})  
        # Real._logger.info('tradeId = {} load trade = {}, config = {}'.format(self.tradeId, self.trade, self.config))  


    def load_data(self):
        if(self.is_batch()):
            self.load_batch_data()
        else:
            if not hasattr(self, 'data'):
                self.data = {
                    'data' : [],
                    'index' : []
                }
            cond_data = {"_id" : {"$gt" : self.data['data'][-1]["_id"]}} if len(self.data['data']) > 0 else {}    
            data = self.data_db[self.trade['params']['code'] + '-' + self.date].find(cond_data).sort([("_id" , 1)])
            cond_index = {"_id" : {"$gt" : self.data['index'][-1]["_id"]}} if len(self.data['index']) > 0 else {}
            if(self.trade['params']['code'].startswith('3')):
                index = self.data_db[Constants.INDEX[5] + '-' + self.date].find(cond_index).sort([("_id" , 1)])
            else:
                index = self.data_db[Constants.INDEX[0] + '-' + self.date].find(cond_index).sort([("_id" , 1)])    
            self.data['data'].extend(data)
            self.data['index'].extend(index)



    def is_batch(self):
        return ',' in self.trade['params']['code']


    def load_batch_data(self):
        if not hasattr(self, 'data'):
            self.data = {
                'data' : {},
                'index' : {}
            }
        codes = self.trade['params']['code'].split(',')
        for code in codes:
            try:
                if code not in self.data['data']:
                    self.data['data'][code] = []
                cond_data = {"_id" : {"$gt" : self.data['data'][code][-1]["_id"]}} if len(self.data['data'][code]) > 0 else {}
                data = self.data_db[code + '-' + self.date].find(cond_data).sort([("_id" , 1)])
                self.data['data'][code].extend(data)
                if code.startswith('3'):
                    if Constants.INDEX[5] not in self.data['index']:
                        self.data['index'][Constants.INDEX[5]] = []
                    cond_index = {"_id" : {"$gt" : self.data['index'][Constants.INDEX[5]][-1]["_id"]}} if len(self.data['index'][Constants.INDEX[5]]) > 0 else {}
                    index = self.data_db[Constants.INDEX[5] + '-' + self.date].find(cond_index).sort([("_id" , 1)])
                    self.data['index'][Constants.INDEX[5]].extend(index)
                else:
                    if Constants.INDEX[0] not in self.data['index']:
                        self.data['index'][Constants.INDEX[0]] = []
                    cond_index = {"_id" : {"$gt" : self.data['index'][Constants.INDEX[0]][-1]["_id"]}} if len(self.data['index'][Constants.INDEX[0]]) > 0 else {}
                    index = self.data_db[Constants.INDEX[0] + '-' + self.date].find(cond_index).sort([("_id" , 1)])
                    self.data['index'][Constants.INDEX[0]].extend(index)
            except Exception as e:
                Real._logger.error('tradeId={} load data {} error {}'.format(self.tradeId, code, e))




    def updateTrade(self, update):
        Real._logger.info('update tradeId={} with update = {}'.format(self.tradeId, update))
        return self.db[self.cols['trades']].update_one({"_id" : ObjectId(self.tradeId)},{"$set" : update})


    def updateConfig(self, update):
        Real._logger.info('update configId={} with update = {}'.format(self.config['_id'], update))
        return self.db[self.cols['configs']].update_one({"_id" : self.config['_id']}, update)


    def get_data(self):
        if(self.is_batch()):
            return self.strategy.get_match_data()
        return self.data['data']
    
    
    def get_code(self):
        if(self.is_batch()):
            return self.get_data()[-1]['code']
        return self.trade['params']['code']

    def createOrder(self):
        data = self.get_data()[-1]
        code = self.get_code()
        price = float(data['price'])
        Real._logger.info(f'start create order for code = {code}, time = {data["time"]}')
        op = self.get_op()
        if(op == 'buy'):
            amount = float(self.trade['params']['volume'])
            if self.is_T0():
                volume = amount
            else:
                volume = int(amount / price / 100) * 100
            if(volume >= 100):
                result = self.createDelegate(code, price, volume, op)
            else:
                result = {'result' : '买入总额不足100股', 'state' : Constants.STATE[3]}
        else:
            volume = int(self.trade['params']['volume'])
            result = self.createDelegate(code, price, volume, op)
        self.updateTrade(result)
        return result
    
    
    def is_T0(self):
        return str(self.strategy.__class__).find('PPT0') >= 0


    def load_config(self):
        self.__header['gw_reqtimestamp'] = f'{int(time()*1000)}'
        self.__header['Cookie'] = self.config['cookie']
        self.__validatekey = self.config['validatekey']


    def createDelegate(self, code, price, volume, op):
        try:
            self.load_config()
            tradeType = 'Buy' if op == 'buy' else 'Sell'
            self.__header['Referer'] = f'https://jy.xzsec.com/Trade/{tradeType}'
            market = 'HA' if code.startswith('6') else 'SA'
            postData = {
                'stockCode': code,
                'price': price,
                'amount': volume,
                'tradeType': tradeType[0],
                'zqmc': self.data['data'][code][-1]['name'],
                'market': market
            }
            if op == 'sell':
                postData['gddm'] = self.config['gddm']
            url = f'https://jy.xzsec.com/Trade/SubmitTradeV2?validatekey={self.__validatekey}'
            response = requests.post(url,data=postData,headers=self.__header)
            Real._logger.info('real tradeId = {}, code = {}, price = {}, volume = {}, op = {}, submit order get response = {}'.format(self.tradeId, code, price, volume, op, response.text))
            result = json.loads(response.text)
            if(result['Status'] == 0):
                op_cn = '买入' if op == 'buy' else '卖出'
                message = '订单提交: 在{},以{}{}[{}] {}股'.format(datetime.now(), price, op_cn, code, volume)
                order = {
                    'result' : {
                        'data' : {
                            'htbh' : result['Data'][0]['Wtbh']
                        }
                    }
                }
                return {'state' : Constants.STATE[2], 'result' : message, 'order' : order}
            return {'state' : Constants.STATE[3], 'result' : result}
        except Exception as e:
            Real._logger.error('mock tradeId = {}, code = {}, price = {}, volume = {}, op = {}, faield with exception = {}'.format(self.tradeId, code, price, volume, op, e))
            return {'state' : Constants.STATE[3], 'result' : '创建订单失败'}


    def cancelOrder(self):
        if('order' not in self.trade or len(self.trade['order']) == 0):
            Real._logger.error('no order found in trade = {}, failde to cancel'.format(self.tradeId))
            update = {'state' : Constants.STATE[3], 'result' : '未找到订单'}
            self.updateTrade(update)
            return update
        htbh = self.trade['order']['result']['data']['htbh']
        today = datetime.now()
        htrq = '{}{}{}'.format(today.year,('0' + str(today.month))[-2:],('0' + str(today.day))[-2:])
        result = self.cancelDelegate(htbh, htrq)
        self.updateTrade(result)
        return result


    def cancelDelegate(self, htbh, wtrq):
        self.load_config()
        self.__header['Referer'] = 'https://jy.xzsec.com/Trade/Buy'   
        self.__header['Accept'] = 'text/plain, */*; q=0.01'   
        self.__header['Accept-Language'] = 'zh-CN,zh;q=0.9'         
        postData = {
            'revokes' : f'{wtrq}_{htbh}'
        }
        try:   
            url = f'https://jy.xzsec.com/Trade/RevokeOrders?validatekey={self.__validatekey}'
            response = requests.post(url,data=postData,headers=self.__header)
            Real._logger.info('real tradeId = {} htbh = {} cancel delegate get response = {}'.format(self.tradeId, htbh, response.text))
            if response.text.find('撤单委托已提交') >= 0:
                return {'state' : Constants.STATE[0], 'result' : '合同[{}]已撤销'.format(htbh)}
            {'state' : Constants.STATE[3], 'result' : response.text}
        except Exception as e:
                Real._logger.error('can deligate [{}] faield, e = {}'.format(htbh, e))
                return {'state' : Constants.STATE[3], 'result' : '合同[{}]撤销失败，请检查配置'.format(htbh)}   


    def reLogin(self):
        return {'result' : 'not allowed', 'state' : Constants.STATE[3]}  


    def check_chengjiao(self, htbh):
        if(self.trade['state'] == Constants.STATE[4] or self.trade['state'] == Constants.STATE[6]):
            return
        update = self.queryChenjiao(htbh)
        if len(update) == 0:
            return
        self.updateTrade(update)
        if(update['state'] == Constants.STATE[4] and self.get_op() == 'buy' and (not self.is_T0())):
            self.updateConfig({ '$inc': { 'curBuyNum': 1 } })
        

    def queryChenjiao(self, htbh):
        try:
            self.load_config()
            self.__header['Referer'] = 'https://jy.xzsec.com/Trade/Sale'
            postData = {
                'qqhs': '10',
                'dwc': ''
            }
            url = f'https://jy.xzsec.com/Search/GetDealData?validatekey={self.__validatekey}'
            response = requests.post(url,data=postData,headers=self.__header)
            Real._logger.info('real tradeId = {} htbh = {} query chengjiao, get response = {}'.format(self.tradeId, htbh, response.text))
            result = json.loads(response.text)
            if(result['Status'] == 0):
                orders = result['Data']
                if(orders is not None and len(orders) > 0):
                    for order in orders:
                        if(order['Wtbh'] == htbh):
                            message = '以{}成交{}股,合同编号{}'.format(order['Cjje'], order['Cjsl'], htbh)
                            state = Constants.STATE[4]
                            if self.is_T0() and self.strategy.op == 'buy':
                                state = Constants.STATE[6]          
                            return {'state' : state, 'result' : message, 'order' : order}
                if 'auto_cancel' in self.trade['params'] and self.trade['params']['auto_cancel'] == '1':
                    return {'state' : Constants.STATE[5], 'result' : '超时未成交，自动取消订单'}
                return {}
            return {'state' : Constants.STATE[3], 'result' : result['Message']}
        except Exception as e:
            Real._logger.error('real tradeId = {} query chengjiao faield e = {}'.format(self.tradeId, e))
            return {'state' : Constants.STATE[3], 'result' : '查询订单[{}]成交状况失败，请检查配置'.format(htbh)}


    


    def init_Config(self):
        self.load_trade_config()
        self.strategyMeta = self.db['strategies'].find_one({"_id" : self.trade['strategyId']})
        Real._logger.info('tradeId = {} load startegy = {}'.format(self.tradeId, self.strategyMeta))
        class_name = self.strategyMeta['url']
        strategyClass = locate('firestone_engine.strategies.{}.{}'.format(class_name, class_name))
        self.strategy = strategyClass()
        if(self.strategy is None):
            Real._logger.error(f'failed to load strategy {class_name}')


    def close(self):
        self.client.close()