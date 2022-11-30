from pathlib import Path
import sys
from beetools import exec_cmd
from git import Repo, exc as git_exc
from pydantic import BaseModel


class CommitMsgSettings(BaseModel):
    msg: str | None = None


class CommitMsgs(BaseModel):
    defcommit: str | None = 'Routine commit'
    DC: str = 'Daily commit'
    RC: str = 'Regular commit'
    HF: str = 'Hotfix'

class CommitDef:
    def __init__(self, p_settings=None, config=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        # The pre-commit hooks does not with self.repo.index.commit. Use
        # beeutils.exec_cmd function to execute it in a session.
        # self.commit_obj = self.repo.index.commit(CommitMsgs().defcommit)
        self.rc = exec_cmd(['git', 'commit', '-m', CommitMsgs().defcommit])
        self.rc = exec_cmd(['git', 'commit', '-m', CommitMsgs().defcommit])
        self.repo.close()
        pass


class CommitCust:
    def __init__(self, p_settings=None, config=None):
        self.settings = CommitMsgSettings(msg=p_settings.msg)
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        # The pre-commit hooks does not with self.repo.index.commit. Use
        # beeutils.exec_cmd function to execute it in a session.
        # self.commit_obj = self.repo.index.commit(self.settings.msg)
        self.rc = exec_cmd(['git', 'commit', '-m', self.settings.msg])
        self.rc = exec_cmd(['git', 'commit', '-m', self.settings.msg])
        self.repo.close()
        pass


class CommitPre:
    def __init__(self, p_settings, config=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        # The pre-commit hooks does not with self.repo.index.commit. Use
        # beeutils.exec_cmd function to execute it in a session.
        if p_settings.msg:
            msg = CommitMsgs().dict()[p_settings.msg.upper()]
            self.rc = exec_cmd(['git', 'commit', '-m', msg])
            if self.rc != 1:
                self.rc = exec_cmd(['git', 'commit', '-m', msg])
        self.repo.close()
        pass
