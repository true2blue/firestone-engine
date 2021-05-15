import unittest
from .TestBasic import TestBase
from firestone_engine.strategies.PPT0 import PPT0
from firestone_engine.Constants import Constants

class TestPPT0(TestBase, unittest.TestCase):
    
    def get_test_config(self):
        return {
            'tradeId' : '5db7e0a555609bb27252edb9',
            'configId' : '5db796e4429e4baab72826a0',
            'data_col' : '300448-2019-12-10',
            'index_col' : 'cyb-2019-12-10'
        }
        
        
    def setUp(self):
        self.baseSetUp()


    def tearDown(self):
        self.baseTearDown()

    def createStrategy(self):
        self.strategy = PPT0()
        
    def runAssert(self):
        self.assertEqual(self.temp_data[-1]['time'], '09:35:00')
        
    def runAssertSell(self):
        self.assertEqual(self.temp_data[-1]['time'], '14:06:36')
        
        
    def testRunWrapper(self):
        self.createStrategy()
        self.temp_data = []
        self.temp_index = []
        i = 0
        while i < len(self.data):
            self.temp_data.append(self.data[i])
            if i < len(self.index):
                self.temp_index.append(self.index[i])
            if(self.strategy.run(self.trade, self.config, self.temp_data, self.temp_index)):
                if self.trade['state'] == Constants.STATE[0]:
                    self.runAssert()
                    self.trade['state'] = Constants.STATE[6]
                elif self.trade['state'] == Constants.STATE[6]:
                    self.runAssertSell()
                    return
            i += 1
        self.runAssert()


if __name__ == "__main__":
    unittest.main()
    
# # to debug in vscode uncomment this block
# import ptvsd
# # 5678 is the default attach port in the VS Code debug configurations
# print("start debug on port 5678")
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()