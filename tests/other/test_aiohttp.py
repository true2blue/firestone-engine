import tushare as ts
import asyncio


async def get_data(l):
    df = await ts.get_realtime_quotes(l)
    print(df)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [asyncio.async(get_data('002639')), asyncio.async(get_data('000793'))]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()