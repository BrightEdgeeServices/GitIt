from pathlib import Path
import sys
from git import Repo, exc as git_exc
from gitignore_parser import parse_gitignore


class ProjectRepo:
    def __init__(self, p_settings=None):
        try:
            # import pdb;pdb.set_trace()
            self.settings = p_settings
            include_lst = ['.gitignore']
            files_to_add = False
            cwd = Path().cwd()
            self.git_repo = Repo(cwd)
            gitignore_pth = cwd / '.gitignore'
            if not gitignore_pth.exists():
                # gitignore_pth.touch()
                gitignore_pth.write_text('.git/\n')
            ignore_match = parse_gitignore(gitignore_pth)
            cur_entries = [Path(x[0][0]) for x in self.git_repo.index.entries.items()]
            dir_contents = list(cwd.glob('**/*'))
            for item in dir_contents:
                if not ignore_match(item) or item == gitignore_pth:
                    if item.is_file():
                        include_lst.append(str(item))
                        if item.relative_to(cwd) not in cur_entries:
                            print(f'Adding {item}')
                            files_to_add = True
            if not files_to_add:
                print('No files to add.')
            self.git_repo.index.add(include_lst)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            sys.exit(2)
        self.git_repo.close()
        pass


def main():
    return ProjectRepo().git_repo
