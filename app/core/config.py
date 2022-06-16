from pydantic import BaseSettings
import base64

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # ElasticSearch
    ES_API: str
    ES_USERNAME: str
    ES_SECRET: str
    DOC_INDEX: str = 'example'

    def encode_credentials(self):
       return base64.b64encode(f'{self.ES_USERNAME}:{self.ES_SECRET}'.encode('ascii')).decode('ascii')

settings = Settings()
