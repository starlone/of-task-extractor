from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    projects_path: Optional[str] = '/home/user/git/*'

    class Config:
        env_file = ".env"
