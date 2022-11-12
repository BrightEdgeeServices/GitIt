'''Testing gitit__init__()'''
import os
from pathlib import Path
import pytest
from git import Repo
from gitit.add.adda import AddToMasterBranchError
from gitit import __main__


@pytest.mark.main
class TestGitIt:
    def test_gitit_with_no_args(self, monkeypatch):
        # monkeypatch.setattr(
        #     'sys.argv',
        #     ['gitit'],
        # )
        with pytest.raises(SystemExit):
            __main__.main()

        pass

    # def test_set_env_with_args(self, monkeypatch):
    #     monkeypatch.setattr(
    #         'sys.argv',
    #         [
    #             "pytest",
    #             "setenv",
    #             "--py-version",
    #             "310",
    #             "--issue-prefix",
    #             "PRE",
    #             "--project-name",
    #             "Project Name",
    #         ],
    #     )
    #
    #     __main__.main()
    #     assert os.environ['GITIT_PY_VER'] == '310'
    #     assert os.environ['GITIT_ISSUE_PREFIX'] == 'PRE'
    #     assert os.environ['GITIT_PROJECT_NAME'] == 'Project Name'
    #     pass


@pytest.mark.adda
class TestAddA:
    def test_adda_clean(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda', '--master'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.adda()
        args = pa.parser.parse_args()
        args.func(args)
        repo = Repo.init(env_setup.dir, bare=False)

        assert [f[0][0] for f in list(repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bug.md',
            '.github/ISSUE_TEMPLATE/config.yaml',
            '.github/workflows/ci.yaml',
            '.github/workflows/release.yml',
            '.gitignore',
            'tracked.txt',
            'tracked/tracked01.py',
            'tracked/tracked02.py',
        ]
        repo.close()
        os.chdir(env_setup.dir.parent)
        pass

    def test_adda_change_file(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda', '--master'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.adda()
        args = pa.parser.parse_args()
        args.func(args)

        repo = Repo(env_setup.dir)
        repo.index.commit("Commit original files")
        Path(env_setup.dir, 'tracked', 'tracked01.py').write_text(
            'This files can be deleted'
        )
        diff = [x.a_path for x in repo.index.diff(None)]
        assert diff == ['tracked/tracked01.py']
        repo.close()

        args.func(args)
        repo = Repo(env_setup.dir)
        assert [x.a_path for x in repo.index.diff(None)] == []
        assert [f[0][0] for f in list(repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bug.md',
            '.github/ISSUE_TEMPLATE/config.yaml',
            '.github/workflows/ci.yaml',
            '.github/workflows/release.yml',
            '.gitignore',
            'tracked.txt',
            'tracked/tracked01.py',
            'tracked/tracked02.py',
        ]

        os.chdir(env_setup.dir.parent)
        pass

    def test_adda_add_new_file(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda', '--master'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.adda()
        args = pa.parser.parse_args()
        args.func(args)

        repo = Repo(env_setup.dir)
        repo.index.commit("Commit original files")
        Path(env_setup.dir, 'tracked', 'tracked03.py').touch()
        assert repo.untracked_files == ['tracked/tracked03.py']
        repo.close()

        args.func(args)
        repo = Repo(env_setup.dir)
        assert [x.a_path for x in repo.index.diff(None)] == []
        assert [f[0][0] for f in list(repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bug.md',
            '.github/ISSUE_TEMPLATE/config.yaml',
            '.github/workflows/ci.yaml',
            '.github/workflows/release.yml',
            '.gitignore',
            'tracked.txt',
            'tracked/tracked01.py',
            'tracked/tracked02.py',
            'tracked/tracked03.py',
        ]

        os.chdir(env_setup.dir.parent)
        pass

    def test_adda_delete_file(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda', '--master'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.adda()
        args = pa.parser.parse_args()
        args.func(args)

        repo = Repo(env_setup.dir)
        repo.index.commit("Commit original files")
        Path(env_setup.dir, 'tracked', 'tracked01.py').unlink()
        assert [x.a_path for x in repo.index.diff(None)] == ['tracked/tracked01.py']
        assert repo.untracked_files == []
        repo.close()

        args.func(args)
        repo = Repo(env_setup.dir)
        assert [x.a_path for x in repo.index.diff(None)] == []
        assert [f[0][0] for f in list(repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bug.md',
            '.github/ISSUE_TEMPLATE/config.yaml',
            '.github/workflows/ci.yaml',
            '.github/workflows/release.yml',
            '.gitignore',
            'tracked.txt',
            'tracked/tracked02.py',
        ]
        repo.close()

        os.chdir(env_setup.dir.parent)
        pass

    def test_adda_no_master(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.adda()
        args = pa.parser.parse_args()
        with pytest.raises(AddToMasterBranchError):
            args.func(args)
        pass
