from fastapi import FastAPI, WebSocket
from broadcaster import Broadcast
from starlette.concurrency import run_until_first_complete


app = FastAPI()
bc = Broadcast('redis://localhost:6379')


@app.on_event('startup')
async def startup():
    await bc.connect()


@app.on_event('shutdown')
async def shutdown():
    await bc.disconnect()


@app.get('/ping')
async def pint():
    return 'pong'


async def receiver(uid: str, ws: WebSocket):
    async for msg in ws.iter_text():
        await bc.publish(channel=uid, message=msg)


async def sender(uid: str, ws: WebSocket):
    async with bc.subscribe(channel=uid) as subs:
        async for i in subs:
            await ws.send_text(i.message)


@app.websocket('/{uid}')
async def room(uid: str, ws: WebSocket):
    await ws.accept()
    await run_until_first_complete(
        (sender, {'uid': uid, 'ws': ws}),
        (receiver, {'uid': uid, 'ws': ws}),
    )
