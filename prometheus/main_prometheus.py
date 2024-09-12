import asyncio

from prometheus_client import start_http_server

from monitox.settings import config
from prometheus.prometheus import update_system_metrics


async def main():
    start_http_server(config.metrics.port)
    asyncio.create_task(update_system_metrics())


if __name__ == "__main__":
    asyncio.run(main())
