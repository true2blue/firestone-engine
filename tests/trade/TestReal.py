import unittest
from firestone_engine.Real import Real
# import ptvsd

class TestReal(unittest.TestCase):


    def setUp(self):
        self.real = Real('69c89bed6ec9aa2688e4daf2', date='2026-03-29')
        self.real.data = {
            'data' : [{
                'name' : '豪能股份'
            }],
        }


    def test_create_delegate(self):
        print(self.real.createDelegate('603809', 10.55, 100, 'sell'))

    # def test_query_chengjiao(self):
    #     print(self.real.queryChenjiao('14186'))

    # def test_cancel_delegate(self):
    #     print(self.real.cancelDelegate('14186', '20241027'))

if __name__ == "__main__":
    #     # 5678 is the default attach port in the VS Code debug configurations
    # print("start debug on port 5678")
    # ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    # ptvsd.wait_for_attach()
    unittest.main()
