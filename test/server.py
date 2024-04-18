from fastapi import FastAPI
from pydantic import BaseModel
from tabulate import tabulate

app = FastAPI()

class ResourceUsage(BaseModel):
    client_id: str
    cpu_percent: float
    memory_percent: float
    upload_speed: float
    download_speed: float

resource_usage_data = {}

@app.post("/resource-usage/")
async def receive_resource_usage(resource_usage: ResourceUsage):
    resource_usage_data[resource_usage.client_id] = resource_usage
    print_resource_usage_table()
    return {"message": "Resource usage received successfully"}

def print_resource_usage_table():
    headers = ["Client ID", "CPU Usage (%)", "Memory Usage (%)", "Upload Speed (MB)", "Download Speed (MB)"]
    rows = []
    for client_id, usage in resource_usage_data.items():
        rows.append([usage.client_id, usage.cpu_percent, usage.memory_percent, usage.upload_speed, usage.download_speed])
    clear_console()
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def clear_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
