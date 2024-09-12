from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

load_dotenv()


class Postgres(BaseSettings):
    host: str = Field(default="localhost", validation_alias="POSTGRES_HOST")
    port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    user: str = Field(default="monitox", validation_alias="POSTGRES_USER")
    password: str = Field(default="monitox", validation_alias="POSTGRES_PASSWORD")
    database: str = Field(default="monitox", validation_alias="POSTGRES_DB")

    @property
    def uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class TelegramBot(BaseSettings):
    token: str = Field(default=None, validation_alias="TG_TOKEN")


class Mistral(BaseSettings):
    api_key: str = Field(validation_alias="MISTRAL_API_KEY")
    model: str = Field(validation_alias="MISTRAL_MODEL")


class LargeLanguageModel(BaseModel):
    mistral: Mistral = Mistral()  # type: ignore[call-arg]


class VulnerabilityModel(BaseSettings):
    vulnerability_url: str = Field(validation_alias="VULNERABILITY_URL")


class MetricsConfig(BaseSettings):
    port: int = Field(default=8001, validation_alias="METRICS_PORT")


class MonitoxConfig(BaseModel):
    postgres: Postgres = Postgres()
    bot: TelegramBot = TelegramBot()
    llm: LargeLanguageModel = LargeLanguageModel()
    vulnerability: VulnerabilityModel = VulnerabilityModel()
    metrics: MetricsConfig = MetricsConfig()


config = MonitoxConfig()
