import unittest
from firestone_engine.Real import Real
import ptvsd

class TestReal(unittest.TestCase):


    def setUp(self):
        self.real = Real('671ddee64f592501c8d5e82b', date='2024-10-27')
        self.real.data = {
            'data' : [{
                'name' : '人工智能ETF'
            }],
        }


    def test_create_delegate(self):
        print(self.real.createDelegate('159819', 0.881, 100, 'buy'))

    def test_query_chengjiao(self):
        print(self.real.queryChenjiao('14186'))

    def test_cancel_delegate(self):
        print(self.real.cancelDelegate('14186', '20241027'))

if __name__ == "__main__":
    #     # 5678 is the default attach port in the VS Code debug configurations
    print("start debug on port 5678")
    ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    ptvsd.wait_for_attach()
    unittest.main()
