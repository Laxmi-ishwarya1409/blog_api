from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):
    DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    
    model_config = SettingsConfigDict(env_file = ".env", extra = "ignore")

Config = settings()