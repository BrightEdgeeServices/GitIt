import os
from pydantic import BaseModel


class EnvSettings(BaseModel):
    py_ver: str | None = None
    issue_prefix: str | None = None
    project_name: str | None = None


class Environment:
    def __init__(self, p_settings):
        self.settings = EnvSettings(
            py_ver=p_settings.py_version,
            issue_prefix=p_settings.issue_prefix,
            project_name=p_settings.project_name,
        )
        self.set_env()
        pass

    def set_env(self):
        if self.settings.py_ver:
            os.environ['GITIT_PY_VER'] = self.settings.py_ver
        elif os.getenv('GITIT_PY_VER') is None:
            os.environ['GITIT_PY_VER'] = ''

        if self.settings.issue_prefix:
            os.environ['GITIT_ISSUE_PREFIX'] = self.settings.issue_prefix
        elif os.getenv('GITIT_ISSUE_PREFIX') is None:
            os.environ['GITIT_ISSUE_PREFIX'] = ''

        if self.settings.project_name:
            os.environ['GITIT_PROJECT_NAME'] = self.settings.project_name
        elif os.getenv('GITIT_PROJECT_NAME') is None:
            os.environ['GITIT_PROJECT_NAME'] = ''
