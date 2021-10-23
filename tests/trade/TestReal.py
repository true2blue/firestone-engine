import unittest
from firestone_engine.Real import Real
import ptvsd

class TestReal(unittest.TestCase):


    def setUp(self):
        self.real = Real('6166f397feeeb90e306a0ef1', date='2021-10-13')
        self.real.data = {
            'data' : {
                '000836' : [{
                    'name' : '富通信息'
                }]
            },
        }


    # def test_create_delegate(self):
    #     print(self.real.createDelegate('000836', 2.65, 100, 'buy'))

    # def test_query_chengjiao(self):
    #     print(self.real.queryChenjiao('94584'))

    def test_cancel_delegate(self):
        print(self.real.cancelDelegate('160745', '20211022'))

if __name__ == "__main__":
    #     # 5678 is the default attach port in the VS Code debug configurations
    print("start debug on port 5678")
    ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    ptvsd.wait_for_attach()
    unittest.main()
