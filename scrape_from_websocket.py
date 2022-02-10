import asyncio
import websockets
from test1 import getHash

def connect(hash):
    async def hello():
        #headers = {'Sec-WebSocket-Key': 'kGWZH/IxoG1cgUwZiA8Xxg=='}
        async with websockets.connect('wss://wss.snai.it/SNWS/ssockGiochiVirtuali?q='+ hash, origin='https://www.snai.it') as websocket:
            message = {"event":"detail_avvenimento_gv","data":{"cod_programma":"23128","num_avvenimento":"75"}}
            greeting = await websocket.recv()
            print(greeting)
            await websocket.send(str(message))
            greeting1 = await websocket.recv()
            print(greeting1)

    asyncio.get_event_loop().run_until_complete(hello())

hash_url = getHash() 

if hash_url != 'CAPTCHA':
  connect(hash_url)


