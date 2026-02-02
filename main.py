from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from fastapi import Query
import csv

from pydantic import BaseModel
from typing import List, Dict
import json
import numpy as np
from pathlib import Path


# Create a FastAPI instance
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"]) # Allow GET requests from all origins
# Or, provide more granular control:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow a specific domain
    allow_credentials=True,  # Allow cookies
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow specific methods
    allow_headers=["*"],  # Allow all headers
)

# Define a path operation decorator for the root URL ("/") with a GET request
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Define another endpoint with a path parameter
@app.get("/api")
def read_item( class_: Optional[List[str]] = Query(None, alias="class") ):
    try:
        csv_file = "q-fastapi.csv"
        data = []
        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                data.append({
                    "studentId": int(row["studentId"]),   # ✅ int
                    "class": str(row["class"]).strip()    # ✅ string
                })

        if not class_:
            return {
            "students": data
        }

        result = [item for item in data if item["class"] in class_]

        return {
            "students": result
        }
    except Exception as e:
        return {"error": str(e)}
    
def read_item( class_: str = Query(..., alias="class") ):
    try:
        csv_file = "q-fastapi.csv"
        data = []
        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "studentId": int(row["studentId"]),   # ✅ int
                    "class": str(row["class"]).strip()    # ✅ string
                })

        result = [item for item in data if item["class"] == class_]

        return {
            "students": result
        }
    except Exception as e:
        return {"error": str(e)}

def read_item():
    try:
        csv_file = "q-fastapi.csv"
        data = []
        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "studentId": int(row["studentId"]),   # ✅ int
                    "class": str(row["class"]).strip()    # ✅ string
                })

        return {
            "students": data
        }
    except Exception as e:
        return {"error": str(e)}
    

DATA_PATH = "q-vercel-latency.json"

with open(DATA_PATH) as f:
    TELEMETRY = json.load(f)


class RequestBody(BaseModel):
    regions: List[str]
    threshold_ms: float


@app.post("/api/latency")
def analyze_latency(body: RequestBody) -> Dict[str, Dict]:
    result = {}

    for region in body.regions:
        records = [r for r in TELEMETRY if r["region"] == region]

        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]

        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 2),
            "breaches": sum(l > body.threshold_ms for l in latencies),
        }

    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)