import unittest
from firestone_engine.Real import Real
import ptvsd

class TestReal(unittest.TestCase):


    def setUp(self):
        self.real = Real('6220bddd91fe522cec3db244', date='2021-10-13')
        self.real.data = {
            'data' : [{
                    'name' : '浙大网新'
            }],
        }


    # def test_create_delegate(self):
    #     print(self.real.createDelegate('600797', 6.54, 100, 'buy'))

    # def test_query_chengjiao(self):
    #     print(self.real.queryChenjiao('94584'))

    # def test_cancel_delegate(self):
    #     print(self.real.cancelDelegate('891', '20211024'))

if __name__ == "__main__":
    #     # 5678 is the default attach port in the VS Code debug configurations
    print("start debug on port 5678")
    ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    ptvsd.wait_for_attach()
    unittest.main()
