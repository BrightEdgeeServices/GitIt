from pathlib import Path
import sys
from git import Repo, exc as git_exc
from pydantic import BaseModel
from gitit.tag import tag


class CommitMsgSettings(BaseModel):
    msg: str | None = None


class CommitMsgs(BaseModel):
    defcommit: str | None = 'Routine commit'
    dc: str = 'Daily commit'
    hf: str = 'Hotfix'


class Push:
    def __init__(self, p_settings=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        # self.repo.git.push()
        origin = self.repo.remotes.origin
        if p_settings.refspec:
            origin.push(refspec=p_settings.refspec)
        else:
            origin.push(all=True)
        self.repo.close()
        pass


class PushTag:
    def __init__(self, p_settings=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        tag.Tag(p_settings)
        origin = self.repo.remotes.origin
        if p_settings.refspec:
            origin.push(refspec=p_settings.refspec)
        else:
            origin.push(all=True)
        self.repo.close()
        pass
