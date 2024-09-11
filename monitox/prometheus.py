from prometheus_client import Counter, Summary, Gauge
import psutil
import asyncio

llm_requests_total = Counter('llm_requests_total', 'Total number of LLM requests')
llm_errors_total = Counter('llm_errors_total', 'Total number of errors in LLM requests')
llm_request_duration = Summary('llm_request_duration_seconds', 'Duration of LLM requests in seconds')

memory_usage = Gauge('memory_usage_bytes', 'Memory usage of the bot')
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage of the bot')

async def update_system_metrics():
    while True:
        memory_usage.set(psutil.virtual_memory().used)
        cpu_usage.set(psutil.cpu_percent())
        await asyncio.sleep(5)

@llm_request_duration.time()
async def track_llm_request_duration(func, *args, **kwargs):
    return await func(*args, **kwargs)
