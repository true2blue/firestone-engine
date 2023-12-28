import asyncio
import aiohttp
import json

async def consume_event_stream():
    headers = {
    'Accept': ' text/event-stream',
    'Accept-Encoding': ' gzip, deflate, br',
    'Accept-Language': ' en,zh-CN;q=0.9,zh;q=0.8',
    'Cache-Control': ' no-cache',
    'Connection': ' keep-alive',
    'Host': ' 63.push2.eastmoney.com',
    'Origin': ' https://quote.eastmoney.com',
    'Referer': ' https://quote.eastmoney.com/zixuan/?from=quotecenter',
    'Sec-Fetch-Dest': ' empty',
    'Sec-Fetch-Mode': ' cors',
    'Sec-Fetch-Site': ' same-site',
    'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': ' "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': ' ?0',
    'sec-ch-ua-platform': ' "Windows"'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get('https://63.push2.eastmoney.com/api/qt/ulist/sse?invt=3&pi=0&pz=2&mpi=2000&secids=0.002862,0.300059&ut=6d2ffaa6a585d612eda28417681d58fb&fields=f12,f13,f19,f14,f139,f148,f2,f4,f1,f125,f18,f3,f152,f5,f30,f31,f32,f6,f8,f7,f10,f22,f9,f112,f100&po=1',headers=headers) as response:
            if response.status == 200:
                async for event in response.content.iter_any():
                    data = event.decode()[6:].strip()
                    print(data)
                    print(json.loads(data))
            else:
                print('Failed to connect to the event stream.')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
tasks = [consume_event_stream()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()