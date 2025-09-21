import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field


class EnvironmentVariables(BaseModel):
    APP_DEBUG: bool | None = None
    APP_WORKERS: int | None = Field(default=None, gt=0)
    RATE_LIMIT_REQ_PER_MIN: int = Field(gt=0)


@lru_cache(maxsize=1)
def get_config() -> EnvironmentVariables:
    load_dotenv()
    return EnvironmentVariables.model_validate(os.environ)
