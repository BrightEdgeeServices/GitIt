from pydantic_settings import BaseSettings


# class Config:
#     VENV_ORGANIZATION_NAME = os.environ.get("VENV_ORGANIZATION_NAME")
#
#     def refresh(self):
#         self.VENV_ORGANIZATION_NAME = os.environ.get("VENV_ORGANIZATION_NAME")
#         pass
class Settings(BaseSettings):
    VENV_ORGANIZATION_NAME: str = "MyOrg"


def get_settings() -> Settings:
    return Settings()
    # pass
