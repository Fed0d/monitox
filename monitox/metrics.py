import psutil
import asyncio

from monitox.bot import memory_usage, cpu_usage

async def update_system_metrics():
    while True:
        memory_usage.set(psutil.virtual_memory().used) 
        cpu_usage.set(psutil.cpu_percent())
        await asyncio.sleep(5) 
