import os


class Config(object):
    GITIT_ISSUE_PREFIX = os.environ.get('GITIT_ISSUE_PREFIX').strip()

    def refresh(self):
        self.GITIT_ISSUE_PREFIX = os.environ.get('GITIT_ISSUE_PREFIX')
        pass
