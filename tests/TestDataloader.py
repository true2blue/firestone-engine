import unittest
import os
import time
from firestone_engine.DFCFDataLoader import DFCFDataLoader

class TestDataloader(unittest.TestCase):

    def setUp(self):
        self.dl = DFCFDataLoader(['000723','300300','601600'])


    def test_get_code_list_from_db(self):
        self.dl.start()
        try:
            while(not self.dl.is_finsih()):
                time.sleep(100)
        except KeyboardInterrupt:
            pass
        finally:
            self.dl.stop()

if __name__ == "__main__":
    # import ptvsd
    # # 5678 is the default attach port in the VS Code debug configurations
    # print("start debug on port 5678")
    # ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    # ptvsd.wait_for_attach()

    os.environ['FR_DB'] = 'firestone'
    unittest.main()
