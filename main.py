import uvicorn
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
async def sse(req: Request, user_id: str = Query(...)):
    redis[str(user_id)] = None
    return EventSourceResponse(generate_events(user_id), media_type="text/event-stream")


async def generate_events(user_id):
    i = 0
    print(redis)
    while user_id in redis:
        if redis[str(user_id)] == 'Both' or i==10:
            yield {
                "event": "message",
                "id": i,
                "data": "close"
            }

            del redis[str(user_id)]

        await asyncio.sleep(2)

        yield {
            "event": "message",
            "id": i,
            "data": redis[str(user_id)]
        }

        i += 1


@app.get('/front')
def change(user_id: str = Query(...)):
    if redis[str(user_id)]:
        redis[str(user_id)] = 'Both'
    else:
        redis[str(user_id)] = 'Front'

    return "hi"


@app.get('/back')
def change(user_id: str = Query(...)):
    if redis[str(user_id)]:
        redis[str(user_id)] = 'Both'
    else:
        redis[str(user_id)] = 'Back'

    return "hi"


if __name__ == '__main__':
    uvicorn.run(__name__ + ":app", host="0.0.0.0", port=5689, log_level="info")
