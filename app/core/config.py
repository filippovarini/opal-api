from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # ElasticSearch
    ES_API: str
    ES_USERNAME: str
    ES_SECRET: str

settings = Settings()

print(settings.dict())