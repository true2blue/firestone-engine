import tushare as ts
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time

async def get_data(l):
    df = await ts.get_realtime_quotes(l)
    print(df)
    
def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [asyncio.async(get_data('002639')), asyncio.async(get_data('000793'))]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == "__main__":
    bgs = BackgroundScheduler()
    trigger = CronTrigger(second='*/10')
    bgs.add_job(run,trigger=trigger)
    bgs.start()
    while True:
        time.sleep(3)
    