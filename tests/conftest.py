'''Create a conftest.py

Define the fixture functions in this file to make them accessible across multiple test files.
'''
from pathlib import Path
import pytest
import sys
from tempfile import mkdtemp
from beetools import rm_tree


sys.path.append('path')


class WorkingDir:
    def __init__(self):
        self.dir = Path(mkdtemp(prefix='gitit_'))


class EnvSetUp:
    def __init__(self, p_make_project_ini=False):
        self.dir = WorkingDir().dir
        pass

    def make_structure(self):
        gitignore_path = self.dir / '.gitignore'
        untracked_dir = self.dir / 'untracked'
        tracked_dir = self.dir / 'tracked'
        gitignore_path.touch()
        gitignore_path.write_text('.git/\nuntracked/\n')
        untracked_dir.mkdir()
        tracked_dir.mkdir()
        (untracked_dir / 'untracked01.py').touch()
        (untracked_dir / 'untracked02.py').touch()
        (tracked_dir / 'tracked01.py').touch()
        (tracked_dir / 'tracked02.py').touch()
        (self.dir / 'tracked.txt').touch()
        pass


@pytest.fixture
def env_setup_self_destruct():
    '''Set up the environment base structure'''
    setup_env = EnvSetUp()
    yield setup_env
    rm_tree(setup_env.dir, p_crash=False)


#
#
# @pytest.fixture
# def working_dir_self_destruct():
#     '''Set up the environment base structure'''
#     working_dir = WorkingDir()
#     yield working_dir
#     rm_tree(working_dir.dir, p_c
