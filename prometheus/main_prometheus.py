import asyncio
from prometheus_client import start_http_server
from prometheus.prometheus import update_system_metrics
from monitox.settings import config

async def main():
    start_http_server(config.metrics.port) 
    asyncio.create_task(update_system_metrics()) 

if __name__ == "__main__":
    asyncio.run(main())