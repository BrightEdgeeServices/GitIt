'''Testing gitit__init__()'''
import os
from pathlib import Path
import pytest
from git import Repo
from gitit.add.add import AddToMasterBranchError
from gitit import __main__


@pytest.mark.main
class TestGitIt:
    def test_gitit_with_no_args(self, monkeypatch):
        monkeypatch.setattr(
            'sys.argv',
            ['gitit'],
        )
        with pytest.raises(SystemExit):
            __main__.main()

        pass


@pytest.mark.add
class TestAdd:
    def test_add_a_clean(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda', '--master'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.add_a()
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

    def test_add_a_change_file(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda', '--master'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.add_a()
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

    def test_add_a_add_new_file(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda', '--master'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.add_a()
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

    def test_add_a_delete_file(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda', '--master'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.add_a()
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

    def test_add_a_no_master(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'adda'])

        repo = Repo.init(env_setup.dir, bare=False)
        repo.close()

        os.chdir(env_setup.dir)
        pa = __main__.ParseArgs()
        pa.add_a()
        args = pa.parser.parse_args()
        with pytest.raises(AddToMasterBranchError):
            args.func(args)
        pass


@pytest.mark.branch
class TestBranch:
    def test_branch_new(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr(
            'sys.argv',
            [
                'pytest',
                'branchnew',
                '--master-branch',
                '--issue',
                '1',
                '--category',
                'feature',
                '--desc',
                'My_first_branch',
            ],
        )

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.index.commit("Commit original files")
        repo.close()
        pa = __main__.ParseArgs()
        pa.branch_new()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert obj.branch_name == repo.head.ref.name
        pass


@pytest.mark.commit
class TestCommit:
    def test_commit_def(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'commitdef'])

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.close()
        pa = __main__.ParseArgs()
        pa.commit_def()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert not repo.is_dirty()
        assert obj.repo.head.ref.commit.message == 'Routine commit\n'
        pass

    def test_commit_cust(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr(
            'sys.argv', ['pytest', 'commitcust', '--msg', 'Custom message']
        )

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.close()
        pa = __main__.ParseArgs()
        pa.commit_cust()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert not repo.is_dirty()
        assert obj.repo.head.ref.commit.message == 'Custom message\n'
        pass

    def test_commit_pre(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'commitpre', '--msg', 'DC'])

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.close()
        pa = __main__.ParseArgs()
        pa.commit_pre()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert not repo.is_dirty()
        assert obj.repo.head.ref.commit.message == 'Daily commit\n'
        pass


@pytest.mark.push
class TestPush:
    def test_push(self, monkeypatch, env_setup_self_destruct):
        env_setup = env_setup_self_destruct
        monkeypatch.setattr('sys.argv', ['pytest', 'push'])
        env_setup.make_structure('loc_repo')

        # new_repo = orig_repo.clone(env_setup)
        loc_repo = Repo.init(env_setup.dir, bare=False)
        loc_repo.git.add(all=True)
        loc_repo.index.commit("Commit original files")
        loc_repo.close()

        rem_repo_dir = env_setup.dir.parent / 'rem_repo'
        rem_repo_dir.mkdir()
        rem_repo = Repo.init(rem_repo_dir, bare=True)

        assert loc_repo.__class__ is Repo  # clone an existing repository
        assert rem_repo.__class__ is Repo  # clone an existing repository

        # repo = Repo.init(env_setup.dir, bare=False)
        # os.chdir(env_setup.dir)
        # repo.git.add(all=True)
        # repo.index.commit("Commit original files")
        # repo.close()
        # pa = __main__.ParseArgs()
        # pa.push()
        # args = pa.parser.parse_args()
        # obj = args.func(args)
        #
        # assert obj.branch_name == repo.head.ref.name
        pass
