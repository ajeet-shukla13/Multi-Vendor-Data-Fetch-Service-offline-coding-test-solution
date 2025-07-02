from fastapi import FastAPI, Request
import httpx
import uvicorn
import asyncio

app = FastAPI()

@app.post("/")
async def async_handler(request: Request):
    data = await request.json()
    request_id = data["request_id"]
    payload = data["payload"]

    # simulate delay and webhook call
    asyncio.create_task(simulate_webhook(request_id, payload))
    return {"status": "accepted"}

async def simulate_webhook(request_id, payload):
    await asyncio.sleep(3)
    webhook_data = {
        "request_id": request_id,
        "result": {**payload, "response": "async-done"}
    }
    await httpx.post("http://api:8000/vendor-webhook/async", json=webhook_data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)
