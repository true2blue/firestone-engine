import logging
from .Constants import Constants
import os
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
import aiohttp
from datetime import datetime, timedelta
from .ProxyManager import ProxyManager
import json

class DFCFDataLoader(object):
    
    _logger = logging.getLogger(__name__)

    _MONFO_URL = '127.0.0.1'

    _DATA_DB = 'firestone-data'
    
    _CODE_FROM_DB = '000000'
    
    _UT = '6d2ffaa6a585d612eda28417681d58fb'
    
    _SERVER_IDX = [f'0{x}' if x < 10 else f'{x}' for x in list(range(0, 100))]
    
    _FIELDS = 'f14,f17,f18,f2,f15,f16,f31,f32,f5,f6,f12'
    
    _HEADERS = {
    'Accept': ' text/event-stream',
    'Accept-Encoding': ' gzip, deflate, br',
    'Accept-Language': ' en,zh-CN;q=0.9,zh;q=0.8',
    'Cache-Control': ' no-cache',
    'Connection': ' keep-alive',
    'Host': f' {_SERVER_IDX[0]}.push2.eastmoney.com',
    'Origin': ' https://quote.eastmoney.com',
    'Referer': ' https://quote.eastmoney.com/zixuan/?from=quotecenter',
    'Sec-Fetch-Dest': ' empty',
    'Sec-Fetch-Mode': ' cors',
    'Sec-Fetch-Site': ' same-site',
    'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': ' "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': ' ?0',
    'sec-ch-ua-platform': ' "Windows"'
    }
    
    def __init__(self, code_list, hours=['9','11','10,13-14'], minutes=['25-59','0-29','*']):
        self.proxyManager = ProxyManager()
        self.use_proxy = False
        self.is_finsih_flag = False
        self.previous_data = {}
        self.original_code_list = code_list
        self.current_code_list = []
        self.client = MongoClient(DFCFDataLoader._MONFO_URL, 27017)
        self.db = self.client[os.environ['FR_DB']]
        self.data_client = MongoClient(DFCFDataLoader._MONFO_URL, 27018)
        self.data_db = self.data_client[DFCFDataLoader._DATA_DB]
        self.scheduler = BackgroundScheduler()
        self.add_job(hours, minutes)
        
        
    def is_load_code_from_db(self):
        return DFCFDataLoader._CODE_FROM_DB in self.original_code_list
    
    def get_code_list_from_db_inner(self, coll, temp_list):
        codes_data = self.db[coll].find({"deleted":False, "params.executeDate" : datetime.now().strftime('%Y-%m-%d')},{"code" : 1, "_id" : 0})
        code_list = [code_data["code"] for code_data in list(codes_data) if code_data["code"] != 'N/A']
        for code in code_list:
            if(',' in code):
                temp_list.extend(code.split(','))
            else:
                temp_list.append(code)

    def get_code_list_from_db(self):
        temp_list = []
        self.get_code_list_from_db_inner('trades', temp_list)
        self.get_code_list_from_db_inner('mocktrades', temp_list)
        code_list = temp_list        
        for code in code_list:
            if(code.startswith('3')):
                if(Constants.INDEX[5] not in code_list):
                    code_list.append(Constants.INDEX[5])
            else:  
                if(Constants.INDEX[0] not in code_list):
                    code_list.append(Constants.INDEX[0])
        code_list.sort()
        return list(set(code_list))
    
    def get_code_list(self):
        if self.is_load_code_from_db():
            return self.get_code_list_from_db()
        codes = [code for code in self.original_code_list if code != 'N/A']
        codes.sort()
        if len(codes) == 0:
            self.is_finsih_flag = True
        return codes
    
    def add_job(self, hours, minutes):
        for i, hour in enumerate(hours):
            trigger = CronTrigger(hour=hour,minute=minutes[i],second='*/3', end_date=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
            if(i == len(hours) - 1):
                self.scheduler.add_job(self.run,id="last_job",trigger=trigger, max_instances=30)
            else:
                self.scheduler.add_job(self.run,trigger=trigger, max_instances=30)
                
                
    def run(self):
        try:
            temp = self.get_code_list()
            if temp != self.current_code_list:
                diff = list(set(temp) - set(self.current_code_list))
                DFCFDataLoader._logger.info('start get the data for {}'.format(diff))
                self.current_code_list = temp
                self.load_data(diff)
        except Exception as e:
            DFCFDataLoader._logger.error(e)
            
            
    def load_data(self, diff):
        list_wrapper = []
        size = len(diff)
        if(size > 50):
            list_size = (size // 50) + (1 if (size % 50) > 0 else 0)
            for i in range(list_size):
                list_wrapper.append(diff[i * 50 : i * 50 + 50])
        else:
            list_wrapper.append(diff)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = []
        if(self.use_proxy):
            for l in list_wrapper:
                tasks.append(asyncio.async(self.get_real_time_data_wrapper(l, proxyManager=self.proxyManager)))               
        else:
            for l in list_wrapper:
                tasks.append(asyncio.async(self.get_real_time_data_wrapper(l)))
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        
        
    def map_code(self, code):
        if code == Constants.INDEX[0] or code.startswith('6'):
            return f'1.{code}'
        elif code == Constants.INDEX[5] or code.startswith('0') or code.startswith('3'):
            return f'0.{code}'
        return None
    
    def divide_100(self, value):
        if isinstance(value, int):
            return value / 100
        return value
    
    def get_value(self, key, data, pre_key, pre_data):
        pre_value = pre_data[pre_key] if pre_data is not None and pre_key in pre_data else None
        if key in data:
            return data[key] if data[key] is not None else pre_value
        return pre_value
    
    def parseAndSaveData(self, data):
        try:
            DFCFDataLoader._logger.info(f'data={data}')
            code = data['f12']
            previous_data = self.previous_data[code] if code in self.previous_data else None
            formated_jsons = {
                'name' : self.get_value('f14', data, 'name', previous_data),
                'open' : self.divide_100(self.get_value('f17', data, 'open', previous_data)),
                'pre_close' : self.divide_100(self.get_value('f18', data, 'pre_close', previous_data)),
                'price' : self.divide_100(self.get_value('f2', data, 'price', previous_data)),
                'high' : self.divide_100(self.get_value('f15', data, 'high', previous_data)),
                'low' : self.divide_100(self.get_value('f16', data, 'low', previous_data)),
                'bid' : self.divide_100(self.get_value('f31', data, 'bid', previous_data)),
                'ask' : self.divide_100(self.get_value('f32', data, 'ask', previous_data)),
                'volume' : self.get_value('f5', data, 'volume', previous_data),
                'amount' : self.get_value('f6', data, 'amount', previous_data),
                'date' : datetime.now().strftime('%Y-%m-%d'),
                'time' : datetime.now().strftime('%H:%M:%S'),
                'code' : self.get_value('f12', data, 'code', previous_data)
            }
            if formated_jsons['code'] is not None:
                self.data_db[formated_jsons['code'] + '-' + formated_jsons['date']].insert(formated_jsons)
                self.previous_data[code] = formated_jsons
        except Exception as e:
            DFCFDataLoader._logger.error(f'save data for data={data} e = {e}')
            
            
    def is_during_the_trade_time(self):
        now = datetime.now().strftime('%H:%M:%S')
        return (now >= '09:30:00' and now <= '11:30:00') or (now >= '13:00:00' and now <= '15:00:00')

            
    async def get_real_time_data_wrapper(self, l, proxyManager = None):
        for server_idx in DFCFDataLoader._SERVER_IDX:
            try:
                while not self.is_during_the_trade_time():
                    await asyncio.sleep(1)
                await self.get_real_time_data(l, server_idx = server_idx, proxyManager = proxyManager)
            except Exception as e:
                DFCFDataLoader._logger.error(f'load data error, server_idx = {server_idx}, e = {e}')
        
    async def get_real_time_data(self, l, server_idx = 0, proxyManager = None):
        DFCFDataLoader._logger.info('start get realtime data for {}'.format(l))
        async with aiohttp.ClientSession() as session:
            codes = [code for code in [self.map_code(code) for code in l] if code is not None]
            url = f"https://{server_idx}.push2.eastmoney.com/api/qt/ulist/sse?invt=3&pi=0&pz={len(codes)}&mpi=2000&secids={','.join(codes)}&ut={DFCFDataLoader._UT}&fields={DFCFDataLoader._FIELDS}&po=1"
            DFCFDataLoader._HEADERS['Host'] = f'{server_idx}.push2.eastmoney.com'
            async with session.get(url,headers=DFCFDataLoader._HEADERS) as response:
                if response.status == 200:
                    async for event in response.content.iter_any():
                        try:
                            data = event.decode()[6:].strip()
                            jsonData = json.loads(data)
                            if 'data' in jsonData and jsonData['data'] is not None:
                                total = jsonData['data']['total']
                                for i in range(total):
                                    if str(i) in jsonData['data']['diff']:
                                        self.parseAndSaveData(jsonData['data']['diff'][str(i)])
                        except Exception as e:
                            DFCFDataLoader._logger.error(f'parse data error {event.decode()}, {e}')
                else:
                    DFCFDataLoader._logger.error('Failed to connect to the event stream, start retry')
                    raise Exception(f'server response {response.status}')
    
    
    def start(self):
        self.scheduler.start()
        DFCFDataLoader._logger.info('job get data for {} is start'.format(self.original_code_list))
        
    def is_finsih(self):
        job = self.scheduler.get_job('last_job')
        return self.is_finsih_flag or job is None or job.next_run_time is None

    def stop(self):
        self.client.close()
        self.scheduler.shutdown(wait=True)
        DFCFDataLoader._logger.info('job get data for {} is stop'.format(self.original_code_list))
        