from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class MetricsConfig(BaseSettings):
    port: int = Field(default=8001, validation_alias="METRICS_PORT")


class PrometheusConfig(BaseSettings):
    metrics: MetricsConfig = MetricsConfig()


config = PrometheusConfig()
