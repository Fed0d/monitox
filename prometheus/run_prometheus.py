import asyncio

import psutil
from prometheus_client import Counter, Gauge, Summary, start_http_server
from settings import config

llm_requests_total = Counter("llm_requests_total", "Total number of LLM requests")
llm_errors_total = Counter("llm_errors_total", "Total number of errors in LLM requests")
llm_request_duration = Summary(
    "llm_request_duration_seconds", "Duration of LLM requests in seconds"
)

memory_usage = Gauge("memory_usage_bytes", "Memory usage of the bot")
cpu_usage = Gauge("cpu_usage_percent", "CPU usage of the bot")


async def update_system_metrics():
    while True:
        memory_usage.set(psutil.virtual_memory().used)
        cpu_usage.set(psutil.cpu_percent())
        await asyncio.sleep(5)


@llm_request_duration.time()
async def track_llm_request_duration(func, *args, **kwargs):
    return await func(*args, **kwargs)


async def main():
    start_http_server(config.metrics.port)
    await asyncio.create_task(update_system_metrics())


if __name__ == "__main__":
    asyncio.run(main())
