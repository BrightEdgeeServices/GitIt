'''Testing gitit__init__()'''
import os
from pathlib import Path
import pytest
from git import Repo
from gitit.add.adda import AddA
from gitit import main


class TestGitIt:
    @pytest.mark.xfail
    def test_gitit_with_no_args(self):
        main.main()
        assert os.environ['GITIT_PY_VER'] is None
        assert os.environ['GITIT_ISSUE_PREFIX'] is None
        assert os.environ['GITIT_PROJECT_NAME'] is None
        pass

    def test_set_env_with_args(self, monkeypatch):
        monkeypatch.setattr(
            'sys.argv',
            [
                "pytest",
                "setenv",
                "--py-version",
                "310",
                "--issue-prefix",
                "PRE",
                "--project-name",
                "Project Name",
            ],
        )

        main.main()
        assert os.environ['GITIT_PY_VER'] == '310'
        assert os.environ['GITIT_ISSUE_PREFIX'] == 'PRE'
        assert os.environ['GITIT_PROJECT_NAME'] == 'Project Name'
        pass

    def test_set_env_with_no_args(self, monkeypatch):
        monkeypatch.setattr('sys.argv', ["pytest", "setenv"])
        main.main()
        assert os.getenv('GITIT_PY_VER') == '310'
        assert os.getenv('GITIT_ISSUE_PREFIX') == 'PRE'
        assert os.getenv('GITIT_PROJECT_NAME') == 'Project Name'
        pass

    def test_adda_clean(self, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        adda = AddA()
        assert [f[0][0] for f in list(adda.git_repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bug.md',
            '.github/ISSUE_TEMPLATE/config.yaml',
            '.github/workflows/ci.yaml',
            '.github/workflows/release.yml',
            '.gitignore',
            'tracked.txt',
            'tracked/tracked01.py',
            'tracked/tracked02.py']
        repo.close()
        os.chdir(env_setup.dir.parent)
        pass

    def test_adda_new_entry(self, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()
        os.chdir(env_setup.dir)
        AddA()
        repo = Repo(env_setup.dir)
        repo.index.commit("Commit original files")
        repo.close()
        Path(env_setup.dir, 'tracked', 'tracked01.py').write_text('This files can be deleted')
        Path(env_setup.dir, 'tracked', 'tracked02.py').write_text('This files can be deleted')
        Path(env_setup.dir, 'tracked', 'tracked03.py').touch()
        adda = AddA()
        assert [f[0][0] for f in list(adda.git_repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bug.md',
            '.github/ISSUE_TEMPLATE/config.yaml',
            '.github/workflows/ci.yaml',
            '.github/workflows/release.yml',
            '.gitignore',
            'tracked.txt',
            'tracked/tracked01.py',
            'tracked/tracked02.py',
            'tracked/tracked03.py'
        ]
        repo = Repo(env_setup.dir)
        repo.index.commit("Commit new and modified")
        Path(env_setup.dir, 'tracked', 'tracked01.py').unlink()
        repo = Repo(env_setup.dir)
        AddA()
        repo.index.commit("Commit new and modified")
        os.chdir(env_setup.dir.parent)
        pass
