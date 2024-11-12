from pymongo import MongoClient
from firestone_engine.strategies.BatchYdls import BatchYdls
from bson import ObjectId
import unittest

class TestBatchYdls(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['firestone-test']
        self.data_client = MongoClient('127.0.0.1', 27018)
        self.db_data = self.data_client['firestone-data']
        self.trade = self.db['mocktrades'].find_one({"_id" : ObjectId('5db7e0a555609bb27252edb8')})
        self.config = self.db['configmocks'].find_one({"_id" : ObjectId('5db796e4429e4baab72826a0')})
        self.is_mock = True
        self.userId = '5d905db9fc84d3224b0eb59c'
        self.by = BatchYdls()
        self.load_data()


    def load_data(self):
        self.data = {
            '300448' : list(self.db_data['300448-2019-12-10'].find()),
            '000993' : list(self.db_data['000993-2019-10-30'].find())
        }
        self.index = {
            'sh' : list(self.db_data['sh-2019-10-30'].find()),
            '399006' : list(self.db_data['399006-2019-12-10'].find())
        }


    def test_batch_ydls(self):
        data = {
            '300448' : [],
            '000993' : []
        }
        index = {
            'sh' : [],
            '399006' : []
        }
        for i in range(4479):
            data['300448'].append(self.data['300448'][i])
            data['000993'].append(self.data['000993'][i])
            index['sh'].append(self.index['sh'][i])
            index['399006'].append(self.index['399006'][i])
            if(self.by.run(self.trade, self.config, self.db, data, index)):
                break
        self.assertEqual(data['300448'][-1]['time'], '09:38:39')


    def tearDown(self):
        self.client.close()


if __name__ == "__main__":
    unittest.main()

# # to debug in vscode uncomment this block
# import ptvsd
# # 5678 is the default attach port in the VS Code debug configurations
# print("start debug on port 5678")
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()