import redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def read_job_from_stream():
    job = r.xread({'jobs_stream': '$'}, block=0, count=1)
    if job:
        _, entries = job[0]
        return entries[0][1]
    return None
