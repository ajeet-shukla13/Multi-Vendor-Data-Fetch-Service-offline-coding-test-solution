from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["jobs_db"]
collection = db["jobs"]

def save_job(job):
    job["status"] = "processing"
    collection.insert_one(job)

def complete_job(request_id, result):
    collection.update_one({"request_id": request_id}, {"$set": {
        "status": "complete",
        "result": result
    }})

def get_job(request_id):
    job = collection.find_one({"request_id": request_id}, {"_id": 0})
    if not job:
        return None
    return {
        "status": job.get("status"),
        "result": job.get("result")
    }

def update_job_from_webhook(data):
    request_id = data.get("request_id")
    complete_job(request_id, data.get("result"))
