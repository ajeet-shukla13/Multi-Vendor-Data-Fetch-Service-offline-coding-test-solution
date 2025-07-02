from fastapi import FastAPI, Request
from uuid import uuid4
import json
import redis

app = FastAPI()
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# end point to accepts json payload from user and return request id
@app.post("/jobs")
async def create_job(request: Request):
    data = await request.json()
    request_id = str(uuid4())
    job = {
        "request_id": request_id,
        "payload": json.dumps(data)  # converted dict to string
    }
    r.xadd("jobs_stream", job)
    return {"request_id": request_id}

# end point to respond with job status for given request id
@app.get("/jobs/{request_id}")
async def get_job_status(request_id: str):
    try:
        from db.mongo import get_job
        job = get_job(request_id)
        if not job:
            return {"status": "not_found"}
        return job
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# end point to recieve webhook callbacks from vendor services
@app.post("/vendor-webhook/{vendor}")
async def vendor_webhook(vendor: str, request: Request):
    from db.mongo import update_job_from_webhook
    data = await request.json()
    update_job_from_webhook(data)
    return {"status": "received"}