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


class BranchNew:
    def __init__(self, p_settings=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        if p_settings.master_branch and self.repo.head.ref.name != 'master':
            self.repo.head.master.checkout()
        elif p_settings.current_branch:
            pass  # Use the current branch
        else:
            pass  # Mmmmmmm......
        self.branch_name = (
            f'{p_settings.category}/{p_settings.issue:0>5}_{p_settings.desc[:20]}'
        )
        self.new_branch = self.repo.git.checkout('HEAD', b=self.branch_name)
        self.repo.close()
        pass
