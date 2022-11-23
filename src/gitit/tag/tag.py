from pathlib import Path
import sys
from git import Repo, exc as git_exc
from pydantic import BaseModel


class CommitMsgs(BaseModel):
    release: str | None


class Tag:
    def __init__(self, p_settings=None):
        self.settings = CommitMsgs(msg=p_settings.release)
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        self.repo.create_tag(
            p_settings.release, ref='master', message=f'v{self.settings.release}'
        )
        pass
