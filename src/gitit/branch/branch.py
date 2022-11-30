from pathlib import Path
import sys
from git import Repo, exc as git_exc


class BranchNew:
    def __init__(self, p_settings=None, config=None):
        cwd = Path().cwd()
        try:
            self.repo = Repo(cwd)
        except git_exc.InvalidGitRepositoryError:
            print('Error: Invalid git repository')
            self.repo.close()
            sys.exit(2)

        if p_settings.stash and self.repo.is_dirty():
            self.repo.git.stash()
        if p_settings.master_branch and self.repo.head.ref.name != 'master':
            self.repo.heads.master.checkout()
        self.branch_name = (
            f'{p_settings.category}/'
            f'{config.GITIT_ISSUE_PREFIX}-{p_settings.issue:0>5}_'
            f'{p_settings.desc[:30].replace(" ", "_")}'
        )
        self.new_branch = self.repo.git.checkout('HEAD', b=self.branch_name)
        print(f'On branch {self.repo.active_branch.name}')
        try:
            self.repo.git.stash('pop')
        except git_exc.GitCommandError as err:
            if err.status != 1:
                print(f'Command:\t{err.command}\nError:\t{err.stderr[1:]}')
        self.repo.close()
        pass
