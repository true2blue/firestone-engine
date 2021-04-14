import tushare as ts
import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [asyncio.async(ts.get_realtime_quotes('002639')), asyncio.async(ts.get_realtime_quotes('000793'))]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()