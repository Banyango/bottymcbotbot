from pydantic.v1 import BaseSettings
from wireup import service


class APIConfig(BaseSettings):
    app_port: int
    app_host: str
    api_version: str
    log_level: str
    path_prefix: str
    secure_cookies: bool
    jwt_secret_key: str


@service
def api_config_provider() -> APIConfig:
    return APIConfig()  # type: ignore
