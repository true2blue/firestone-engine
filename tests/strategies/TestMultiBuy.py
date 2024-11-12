import unittest
from .TestBasic import TestBase
from firestone_engine.strategies.MultiBuy import MultiBuy
from firestone_engine.Constants import Constants

class TestPPT0(TestBase, unittest.TestCase):
    
    def get_test_config(self):
        return {
            'tradeId' : '5db7e0a555609bb27252edb1',
            'configId' : '5db796e4429e4baab72826a0',
            'data_col' : '300448-2019-12-10',
            'index_col' : '399006-2019-12-10'
        }
        
        
    def setUp(self):
        self.baseSetUp()


    def tearDown(self):
        self.baseTearDown()

    def createStrategy(self):
        self.strategy = MultiBuy()
        
    def runAssert1(self):
        self.assertEqual(self.temp_data[-1]['time'], '09:30:03')
        
    def runAssert2(self):
        self.assertEqual(self.temp_data[-1]['time'], '09:31:57')

    def runAssert3(self):
        self.assertEqual(self.temp_data[-1]['time'], '09:32:12')
        
        
    def testRunWrapper(self):
        self.createStrategy()
        self.temp_data = []
        self.temp_index = []
        i = 0
        count = 0
        while i < len(self.data):
            self.temp_data.append(self.data[i])
            if i < len(self.index):
                self.temp_index.append(self.index[i])
            if(self.strategy.run(self.trade, self.config, self.temp_data, self.temp_index)):
                if self.trade['state'] == Constants.STATE[0]:
                    self.runAssert1()
                    self.trade['state'] = Constants.STATE[7]
                    count = 1
                elif self.trade['state'] == Constants.STATE[7]:
                    if count == 1:
                        self.runAssert2()
                        count += 1
                    else:
                        self.runAssert3()
                        return
            i += 1


if __name__ == "__main__":
    unittest.main()
    
# to debug in vscode uncomment this block
import ptvsd
# 5678 is the default attach port in the VS Code debug configurations
print("start debug on port 5678")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()