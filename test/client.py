import asyncio
import aiohttp
import psutil
import time
import uuid

async def send_resource_usage():

    client_id = str(uuid.uuid4())
    last_bytes_sent = psutil.net_io_counters().bytes_sent
    last_bytes_recv = psutil.net_io_counters().bytes_recv
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        while True:
            current_bytes_sent = psutil.net_io_counters().bytes_sent
            current_bytes_recv = psutil.net_io_counters().bytes_recv
            elapsed_time = time.time() - start_time
            if elapsed_time == 0:
                upload_speed = (current_bytes_sent - last_bytes_sent) / 1000 / 1000 # mb
                download_speed = (current_bytes_recv - last_bytes_recv) / 1000 / 1000 # mb
            else:
                upload_speed = (current_bytes_sent - last_bytes_sent) / elapsed_time / 1000 / 1000 # mb
                download_speed = (current_bytes_recv - last_bytes_recv) / elapsed_time / 1000 / 1000 # mb
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent

            payload = {
                "client_id": client_id,
                "upload_speed": upload_speed,
                "download_speed": download_speed,
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent
            }
            async with session.post("http://localhost:8000/resource-usage/", json=payload) as response:
                if response.status != 200:
                    print("Failed to send resource usage data to server")
                else:
                    print("Resource usage data sent successfully")
            last_bytes_sent = current_bytes_sent
            last_bytes_recv = current_bytes_recv
            start_time = time.time()
            await asyncio.sleep(1) 

if __name__ == "__main__":
    asyncio.run(send_resource_usage())
