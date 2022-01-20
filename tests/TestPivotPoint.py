import unittest
import tushare
import json
import asyncio
from src.firestone_engine.Utils import Utils

class TestPivotPoint(unittest.TestCase):


    async def get_data(self, codes):
        points = 7
        df = await tushare.get_realtime_quotes(codes)
        json_list = json.loads(df.to_json(orient='records'))
        for data in json_list:
            code = data['code']
            pre_high = float(data['high'])
            pre_low = float(data['low'])
            pre_close = float(data['price'])
            pp = (pre_high + pre_low + pre_close) / 3
            r1 = 2 * pp - pre_low
            r2 = pp + pre_high - pre_low
            r3 = pre_high + 2 * (pp - pre_low)
            s1 = 2 * pp - pre_high
            s2 = pp - pre_high + pre_low
            s3 = pre_low - 2 * (pre_high - pp)
            sm1 = (pp + s1) / 2
            sm2 = (s1 + s2) / 2
            sm3 = (s2 + s3) / 2
            rm1 = (pp + r1) / 2
            rm2 = (r1 + r2) / 2
            rm3 = (r2 + r3) / 2
            if points == 13:
                self.pp = {
                    'r3' : Utils.round_dec(r3),
                    'rm3' : Utils.round_dec(rm3),
                    'r2' : Utils.round_dec(r2),
                    'rm2' : Utils.round_dec(rm2),
                    'r1' : Utils.round_dec(r1),
                    'rm1' : Utils.round_dec(rm1),
                    'pp' : Utils.round_dec(pp),
                    'sm1' : Utils.round_dec(sm1),
                    's1' : Utils.round_dec(s1),
                    'sm2' : Utils.round_dec(sm2),
                    's2' : Utils.round_dec(s2),
                    'sm3' : Utils.round_dec(sm3),
                    's3' : Utils.round_dec(s3)
                }
            else:
                self.pp = {
                    'r3' : Utils.round_dec(r3),
                    'r2' : Utils.round_dec(r2),
                    'r1' : Utils.round_dec(r1),
                    'pp' : Utils.round_dec(pp),
                    's1' : Utils.round_dec(s1),
                    's2' : Utils.round_dec(s2),
                    's3' : Utils.round_dec(s3)
                }
            print(code)
            print(self.pp)

    
    def setUp(self):
        pass

    def test(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [asyncio.async(self.get_data(['601007', '000676', '300067', '002177', '603636']))]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


    def tearDown(self):
        pass



if __name__ == "__main__":
    unittest.main()