"""Create a conftest.py

Define the fixture functions in this file to make them accessible across multiple test files.
"""

from pathlib import Path
from tempfile import mkdtemp
from tempfile import TemporaryDirectory

import pytest
from beetools import rm_tree


# sys.path.append('path')


class WorkingDir:
    def __init__(self, p_secure=True):
        if p_secure:
            self.dir = Path(mkdtemp(prefix='gitit_'))
        else:
            self.dir = Path(TemporaryDirectory())


class EnvSetUp:
    def __init__(self, p_secure=True):
        self.dir = WorkingDir(p_secure).dir
        self.secure = p_secure
        pass

    def make_structure(self, p_sub_dir=None):
        if p_sub_dir:
            self.dir = self.dir / p_sub_dir
            self.dir.mkdir()
        gitignore_path = self.dir / '.gitignore'
        untracked_dir = self.dir / 'untracked'
        tracked_dir = self.dir / 'tracked'
        github_dir = self.dir / '.github'
        gitignore_path.touch()
        # gitignore_path.write_text('.git/\nuntracked/\n')
        gitignore_path.write_text('untracked/\n')
        untracked_dir.mkdir()
        tracked_dir.mkdir()
        Path(github_dir, 'ISSUE_TEMPLATE').mkdir(parents=True, exist_ok=True)
        Path(github_dir, 'workflows').mkdir(parents=True, exist_ok=True)
        (self.dir / 'tracked.txt').touch()
        (untracked_dir / 'untracked01.py').touch()
        (untracked_dir / 'untracked02.py').touch()
        (tracked_dir / 'tracked01.py').touch()
        (tracked_dir / 'tracked02.py').touch()
        (github_dir / 'ISSUE_TEMPLATE' / 'bugfix.md').touch()
        (github_dir / 'ISSUE_TEMPLATE' / 'config.yaml').touch()
        (github_dir / 'workflows' / 'ci.yaml').touch()
        (github_dir / 'workflows' / 'release.yml').touch()
        pass


@pytest.fixture
def env_setup_secure_self_destruct():
    """Set up the environment base structure"""
    setup_env = EnvSetUp()
    yield setup_env
    rm_tree(setup_env.dir, p_crash=False)


@pytest.fixture
def env_setup_unsecure_self_destruct():
    """Set up the environment base structure"""
    setup_env = EnvSetUp(p_secure=False)
    yield setup_env
    rm_tree(setup_env.dir, p_crash=False)
