from pathlib import Path
import sys
from git import Repo, exc as git_exc
from pydantic import BaseModel
from beetools import msg_error


class AddASettings(BaseModel):
    master: bool | None = None


class AddA:
    def __init__(self, p_settings=None, config=None):
        self.settings = AddASettings(master=p_settings.master)
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        if (
            self.repo.active_branch.name not in ['main', 'master']
            or self.settings.master
        ):
            files_to_add = [
                x.a_path for x in self.repo.index.diff(None)
            ] + self.repo.untracked_files
            print(f'On branch {self.repo.active_branch.name}')
            for filename in files_to_add:
                print(f'Adding {filename}')
            self.repo.git.add(all=True)
            if not files_to_add:
                print('No files to add.')
        else:
            raise AddToMasterBranchError
        self.repo.close()
        pass


class AddToMasterBranchError(Exception):
    def __init__(self):
        print(
            msg_error(
                '\nCannot add files to repository on "master" or "main" branch, unless --master switch is set.\n'
            )
        )
        pass
