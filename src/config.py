import os


class Config:
    GITIT_ISSUE_PREFIX = os.environ.get('GITIT_ISSUE_PREFIX').strip()

    def refresh(self):
        self.GITIT_ISSUE_PREFIX = os.environ.get('GITIT_ISSUE_PREFIX')
        pass
