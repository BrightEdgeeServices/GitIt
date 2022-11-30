import configparser
from pathlib import Path
import sys
from git import Repo, exc as git_exc
from gitit.tag import tag

# from pydantic import BaseModel
from gitit.tag import tag


class PushAll:
    def __init__(self, p_settings=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        origin = self.repo.remotes.origin
        origin.push(all=True)
        print(f'On branch {self.repo.active_branch.name}')
        self.repo.close()
        pass


class PushMaster:
    def __init__(self, p_settings=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        origin = self.repo.remotes.origin
        origin.push(refspec='master')
        print(f'On branch {self.repo.active_branch.name}')
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

        if not p_settings.release:
            config = configparser.ConfigParser()
            filename = Path(self.repo.working_dir, 'setup.cfg')
            config.read(filename)
            p_settings.release = config['metadata']['version']
        self.rc = tag.Tag(p_settings)
        origin = self.repo.remotes.origin
        origin.push(tags=True)
        print(f'On branch {self.repo.active_branch.name}')
        self.repo.close()
        pass


class PushWork:
    def __init__(self, p_settings=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        origin = self.repo.remotes.origin
        origin.push(refspec=self.repo.active_branch.name)
        print(f'On branch {self.repo.active_branch.name}')
        self.repo.close()
        pass
