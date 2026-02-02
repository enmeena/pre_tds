from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from fastapi import Query
import csv


# Create a FastAPI instance
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"]) # Allow GET requests from all origins
# Or, provide more granular control:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Allow a specific domain
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)