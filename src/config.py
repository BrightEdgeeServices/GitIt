import os


class Config:
    VENV_INSTITUTION = os.environ.get("VENV_INSTITUTION").strip()

    def refresh(self):
        self.VENV_INSTITUTION = os.environ.get("GITIT_ISSUE_PREFIX")
        pass
