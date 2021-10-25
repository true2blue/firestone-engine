import unittest
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

class TestSchedule(unittest.TestCase):
    
    
    def setUp(self):
        self.data = {
            'a' : 1
        }
        self.scheduler = BackgroundScheduler()
        # self.trigger = CronTrigger(hour='*',minute='*',second='*/10')
        self.trigger2 = CronTrigger(hour='*',minute='*',second='*/3')


    def check_chengjiao(self, htbh):
        print(f'id={id(self)} ,{datetime.now()}, htbh={htbh}, a={self.data["a"]}')
        self.data['a'] += 1
        # print(f'get job2 = {self.scheduler.get_job("check_chengjiao2")}')


    def test_schedule(self):
        self.scheduler.add_job(self.check_chengjiao,kwargs={'htbh' : 3}, trigger=self.trigger2, id='check_chengjiao2')
        self.scheduler.start()
        # self.scheduler.add_job(self.check_chengjiao,kwargs={'htbh' : 10}, trigger=self.trigger, id='check_chengjiao')
        try:
            job = self.scheduler.get_job('check_chengjiao2')
            while job is not None and job.next_run_time is not None:
                job = self.scheduler.get_job('check_chengjiao2')
                time.sleep(100)
        except Exception as e:
            print(e)


    def tearDown(self):
        self.scheduler.shutdown(wait=False)


if __name__ == "__main__":
    unittest.main()