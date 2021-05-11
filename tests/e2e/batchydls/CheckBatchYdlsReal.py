from firestone_engine.Real import Real
import unittest

class CheckBatchYdlsReal(unittest.TestCase):

    def setUp(self):
        self.real = Real('5db7e0a555609bb27252edb8', date='2019-12-10')
        self.real.init_Config()
        self.real.load_trade()
        
    def testTradeState(self):
        self.assertEqual(self.real.trade['state'], '已提交')
        self.assertEqual(self.real.trade['result'], '订单已提交，请在客户端查看')

    def tearDown(self):
        self.real.close()

if __name__ == "__main__":
    unittest.main()