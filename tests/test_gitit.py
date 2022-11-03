'''Testing gitit__init__()'''
import os
from pathlib import Path
import pytest
from git import Repo
from gitit import gitit
from add import adda


class TestGitIt:
    @pytest.mark.xfail
    def test_gitit_with_no_args(self, monkeypatch):
        # monkeypatch.setattr(
        #     'sys.argv',
        #     ["pytest", "set_env", "--py-version", "310", "--issue-prefix", "PRE", "--project-name", "Project Name"]
        # )

        gitit.main()
        assert os.environ['GITIT_PY_VER'] is None
        assert os.environ['GITIT_ISSUE_PREFIX'] is None
        assert os.environ['GITIT_PROJECT_NAME'] is None
        pass

    def test_set_env_with_args(self, monkeypatch):
        monkeypatch.setattr(
            'sys.argv',
            [
                "pytest",
                "set_env",
                "--py-version",
                "310",
                "--issue-prefix",
                "PRE",
                "--project-name",
                "Project Name",
            ],
        )

        gitit.main()
        assert os.environ['GITIT_PY_VER'] == '310'
        assert os.environ['GITIT_ISSUE_PREFIX'] == 'PRE'
        assert os.environ['GITIT_PROJECT_NAME'] == 'Project Name'
        pass

    def test_set_env_with_no_args(self, monkeypatch):
        monkeypatch.setattr('sys.argv', ["pytest", "set_env"])
        gitit.main()
        assert os.getenv('GITIT_PY_VER') == '310'
        assert os.getenv('GITIT_ISSUE_PREFIX') == 'PRE'
        assert os.getenv('GITIT_PROJECT_NAME') == 'Project Name'
        pass

    def test_adda_clean(self, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo = adda.ProjectRepo()
        assert [f[0][0] for f in list(repo.git_repo.index.entries.items())] == [
            '.gitignore',
            'tracked.txt',
            'tracked/tracked01.py',
            'tracked/tracked02.py',
        ]
        os.chdir(env_setup.dir.parent)
        pass

    def test_adda_new_entry(self, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo = adda.ProjectRepo()
        Path(env_setup.dir, 'tracked', 'tracked03.py').touch()
        repo = adda.ProjectRepo()
        assert [f[0][0] for f in list(repo.git_repo.index.entries.items())] == [
            '.gitignore',
            'tracked.txt',
            'tracked/tracked01.py',
            'tracked/tracked02.py',
            'tracked/tracked03.py',
        ]
        os.chdir(env_setup.dir.parent)
        pass
