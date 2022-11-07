from pathlib import Path
import sys
from git import Repo, exc as git_exc
# from gitignore_parser import parse_gitignore


class AddA:
    def __init__(self, p_settings=None):
        self.settings = p_settings
        cwd = Path().cwd()
        try:
            self.git_repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.git_repo.close()
            sys.exit(2)

        files_to_add = [x.a_path for x in self.git_repo.index.diff(None)] \
            + self.git_repo.untracked_files
        for filename in files_to_add:
            print(f'Adding {filename}')
        self.git_repo.git.add(all = True)
        if not files_to_add:
            print('No files to add.')
        self.git_repo.close()
        pass

#
# def main():
#     return ProjectRepo().git_repo
