from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse
import asyncio
import time


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_headers=["*"],
)

redis = {}

@app.get("/")
async def sse(req: Request, test: str = Query(...)):
    redis[str(test)] = None
    return EventSourceResponse(generate_events(test), media_type="text/event-stream")


async def generate_events(test):
    i=0
    while True:
        if redis[str(test)] == 'Both':
            break

        await asyncio.sleep(2)

        yield {
            "event": "message",
            "id": i,
            "data": redis
        }

        i+=1


@app.get('/front')
def change(test: str = Query(...)):
    if redis[str(test)]:
        redis[str(test)] = 'Both'
    else:
        redis[str(test)] = 'Front'

    return "hi"

@app.get('/frobacknt')
def change(test: str = Query(...)):
    if redis[str(test)]:
        redis[str(test)] = 'Both'
    else:
        redis[str(test)] = 'Back'

    return "hi"