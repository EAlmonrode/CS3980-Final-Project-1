import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = os.path.join(os.path.dirname(__file__),'.env')
load_dotenv(dotenv_path=env_path)

class MyConfig(BaseSettings):
    connection_string: str
    secret_key: str

@lru_cache()
def get_settings():
    return MyConfig()



