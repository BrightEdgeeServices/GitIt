from pathlib import Path
import sys
from git import Repo, exc as git_exc
from pydantic import BaseModel


class CommitMsgSettings(BaseModel):
    msg: str | None = None


class CommitMsgs(BaseModel):
    defcommit: str | None = 'Routine commit'
    dc: str = 'Daily commit'
    hf: str = 'Hotfix'


class CommitDef:
    def __init__(self, p_settings=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        self.commit_obj = self.repo.index.commit(CommitMsgs().defcommit)
        self.repo.close()
        pass


class CommitCust:
    def __init__(self, p_settings=None):
        self.settings = CommitMsgSettings(msg=p_settings.msg)
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        self.commit_obj = self.repo.index.commit(self.settings.msg)
        self.repo.close()
        pass


class CommitPre:
    def __init__(self, p_settings):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        self.commit_obj = self.repo.index.commit(
            CommitMsgs().dict()[p_settings.msg.lower()]
        )
        self.repo.close()
        pass


# class AddToMasterBranchError(Exception):
#     def __init__(self):
#         print(
#             msg_error(
#                 '\nCannot add files to repository on "master" or "main" branch, unless --master switch is set.\n'
#             )
#         )
#         pass
