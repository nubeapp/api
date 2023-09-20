from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    url: str
    service_id: str
    template_id: str
    public_key: str
    private_key: str

    class Config:
        env_file = ".env"

settings = Settings()