import sys
from pathlib import Path

from beetools import msg_error
from git import exc as git_exc
from git import Repo
from pydantic import BaseModel


class CommitMsgs(BaseModel):
    release: str | None


class Tag:
    def __init__(self, p_settings=None):
        self.settings = CommitMsgs(release=p_settings.release)
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        try:
            self.tag = self.repo.create_tag(
                p_settings.release,
                ref='master',
                message=f'v{self.settings.release}',
                annotate=True,
            )
        except git_exc.GitCommandError as err:
            print(msg_error(f'\nStatus:\t\t{err.status}\nCommand:\t{err.command}\nMessage{err.stderr}'))
            sys.exit(2)
        pass
