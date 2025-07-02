import time
import json
import redis
import httpx

from db.mongo import save_job, complete_job

r = redis.Redis(host='redis', port=6379, decode_responses=True)

RATE_LIMITS = {
    "sync": {"last_call": 0, "delay": 1},
    "async": {"last_call": 0, "delay": 1}
}

def rate_limited(vendor):
    now = time.time()
    last = RATE_LIMITS[vendor]["last_call"]
    delay = RATE_LIMITS[vendor]["delay"]
    if now - last < delay:
        time.sleep(delay - (now - last))
    RATE_LIMITS[vendor]["last_call"] = time.time()

def clean_data(data):
    result = {}
    for k, v in data.items():
        if isinstance(v, str):
            v = v.strip()
        if "email" not in k.lower() and "phone" not in k.lower():
            result[k] = v
    return result

def choose_vendor(payload):
    return "sync" if payload.get("type") == "sync" else "async"

while True:
    job_data = r.xread({'jobs_stream': '0'}, block=0, count=1)
    if not job_data:
        continue

    _, entries = job_data[0]
    job = entries[0][1]
    print("Picked Job:", job)

    request_id = job["request_id"]
    payload = json.loads(job["payload"].replace("'", '"'))

    save_job({"request_id": request_id, "payload": payload})

    vendor = choose_vendor(payload)
    rate_limited(vendor)

    try:
        if vendor == "sync":
            res = httpx.post("http://sync-vendor:9000", json={"request_id": request_id, "payload": payload})
            cleaned = clean_data(res.json()["result"])
            complete_job(request_id, cleaned)
        else:
            httpx.post("http://async-vendor:9001", json={"request_id": request_id, "payload": payload})
            # Wait for webhook to complete
    except Exception as e:
        print(f"Error processing job: {e}")
