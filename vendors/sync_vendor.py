from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/")
async def sync_handler(request: Request):
    data = await request.json()
    payload = data.get("payload", {})
    return {"result": {**payload, "response": "sync-done"}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
