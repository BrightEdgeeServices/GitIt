"""Testing gitit__init__()"""
import os
from pathlib import Path

import pytest
from git import Repo

from config import Config
from gitit import __main__
from gitit.add.add import AddToMasterBranchError


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
    def test_add_a_clean(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
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
            '.github/ISSUE_TEMPLATE/bugfix.md',
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

    def test_add_a_change_file(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
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
        repo.index.commit('Commit original files')
        Path(env_setup.dir, 'tracked', 'tracked01.py').write_text('This files can be deleted')
        diff = [x.a_path for x in repo.index.diff(None)]
        assert diff == ['tracked/tracked01.py']
        repo.close()

        args.func(args)
        repo = Repo(env_setup.dir)
        assert [x.a_path for x in repo.index.diff(None)] == []
        assert [f[0][0] for f in list(repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bugfix.md',
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

    def test_add_a_add_new_file(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
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
        repo.index.commit('Commit original files')
        Path(env_setup.dir, 'tracked', 'tracked03.py').touch()
        assert repo.untracked_files == ['tracked/tracked03.py']
        repo.close()

        args.func(args)
        repo = Repo(env_setup.dir)
        assert [x.a_path for x in repo.index.diff(None)] == []
        assert [f[0][0] for f in list(repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bugfix.md',
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

    def test_add_a_delete_file(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
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
        repo.index.commit('Commit original files')
        Path(env_setup.dir, 'tracked', 'tracked01.py').unlink()
        assert [x.a_path for x in repo.index.diff(None)] == ['tracked/tracked01.py']
        assert repo.untracked_files == []
        repo.close()

        args.func(args)
        repo = Repo(env_setup.dir)
        assert [x.a_path for x in repo.index.diff(None)] == []
        assert [f[0][0] for f in list(repo.index.entries.items())] == [
            '.github/ISSUE_TEMPLATE/bugfix.md',
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

    def test_add_a_no_master(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
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
    @pytest.mark.parametrize(
        'param',
        [
            [
                '-m',
                '-i',
                '1',
                '-c',
                'feature',
                '--d',
                'My_first_branch',
                '-s',
            ],
            ['-b', '-i', '1', '-c', 'feature', '--d', 'My_first_branch'],
        ],
    )
    def test_branch_new_clean(self, monkeypatch, env_setup_secure_self_destruct, param):
        env_setup = env_setup_secure_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'branchnew'] + param)
        config = Config()
        config.VENV_INSTITUTION = 'BEE'

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.index.commit('Commit original files')
        repo.close()
        pa = __main__.ParseArgs()
        pa.branch_new()
        args = pa.parser.parse_args()
        obj = args.func(args, config)

        assert obj.branch_name == repo.head.ref.name
        pass

    @pytest.mark.parametrize(
        'param',
        [
            [
                '-m',
                '-i',
                '1',
                '-c',
                'feature',
                '--d',
                'My_first_branch',
                '-s',
            ],
            ['-b', '-i', '1', '-c', 'feature', '--d', 'My_first_branch'],
        ],
    )
    def test_branch_new_untracked(self, monkeypatch, env_setup_secure_self_destruct, param):
        env_setup = env_setup_secure_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'branchnew'] + param)
        config = Config()
        config.VENV_INSTITUTION = 'BEE'

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.index.commit('Commit original files')
        (env_setup.dir / 'setup.cfg').touch()
        # repo.git.add(all = True)
        repo.close()
        pa = __main__.ParseArgs()
        pa.branch_new()
        args = pa.parser.parse_args()
        obj = args.func(args, config)

        assert obj.branch_name == repo.head.ref.name
        pass

    @pytest.mark.parametrize(
        'param',
        [
            [
                '-m',
                '-i',
                '1',
                '-c',
                'feature',
                '--d',
                'My_first_branch',
                '-s',
            ],
            ['-b', '-i', '1', '-c', 'feature', '--d', 'My_first_branch'],
        ],
    )
    def test_branch_new_tracked(self, monkeypatch, env_setup_secure_self_destruct, param):
        env_setup = env_setup_secure_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'branchnew'] + param)
        config = Config()
        config.VENV_INSTITUTION = 'BEE'

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.index.commit('Commit original files')
        (env_setup.dir / 'setup.cfg').touch()
        repo.git.add(all=True)
        repo.close()
        pa = __main__.ParseArgs()
        pa.branch_new()
        args = pa.parser.parse_args()
        obj = args.func(args, config)

        assert obj.branch_name == repo.head.ref.name
        pass

    @pytest.mark.parametrize(
        'param',
        [
            [
                '-m',
                '-i',
                '1',
                '-c',
                'feature',
                '--d',
                'My_first_branch',
                '-s',
            ],
            ['-b', '-i', '1', '-c', 'feature', '--d', 'My_first_branch'],
        ],
    )
    def test_branch_new_not_on_master(self, monkeypatch, env_setup_secure_self_destruct, param):
        env_setup = env_setup_secure_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'branchnew'] + param)
        config = Config()
        config.VENV_INSTITUTION = 'BEE'

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.index.commit('Commit original files')
        repo.git.checkout('HEAD', b='Test_branch')
        (env_setup.dir / 'commited.txt').write_text('Delete me')
        repo.git.add(all=True)
        (env_setup.dir / 'setup.cfg').touch()
        (env_setup.dir / 'tracked.txt').write_text('Delete me')
        repo.close()
        pa = __main__.ParseArgs()
        pa.branch_new()
        args = pa.parser.parse_args()
        obj = args.func(args, config)

        assert obj.branch_name == repo.head.ref.name
        pass


@pytest.mark.commit
class TestCommit:
    def test_commit_def(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'commitdef'])

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.git.config('user.email', 'somebody@everywhere.com', local=True)
        repo.git.config('user.name', 'Soembody Somewhere', local=True)
        repo.close()
        pa = __main__.ParseArgs()
        pa.commit_def()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert not repo.is_dirty()
        assert obj.repo.head.ref.commit.message == 'Routine commit\n'
        pass

    def test_commit_cust(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'commitcust', '--msg', 'Custom message'])

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.git.config('user.email', 'somebody@everywhere.com', local=True)
        repo.git.config('user.name', 'Soembody Somewhere', local=True)
        repo.close()
        pa = __main__.ParseArgs()
        pa.commit_cust()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert not repo.is_dirty()
        assert obj.repo.head.ref.commit.message == 'Custom message\n'
        pass

    @pytest.mark.parametrize(
        'param',
        [
            ['DC'],
            # []
        ],
    )
    def test_commit_pre(self, monkeypatch, env_setup_secure_self_destruct, param):
        env_setup = env_setup_secure_self_destruct
        env_setup.make_structure()
        monkeypatch.setattr('sys.argv', ['pytest', 'commitpre'] + param)

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.git.config('user.email', 'somebody@everywhere.com', local=True)
        repo.git.config('user.name', 'Soembody Somewhere', local=True)
        repo.close()
        pa = __main__.ParseArgs()
        pa.commit_pre()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert not repo.is_dirty()
        assert obj.repo.head.ref.commit.message == 'Daily commit\n'
        pass


@pytest.mark.push
@pytest.mark.push
class TestPush:
    def test_push_all(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
        monkeypatch.setattr('sys.argv', ['pytest', 'pushall'])
        env_setup.make_structure('loc_repo')

        loc_repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        loc_repo.git.add(all=True)
        loc_repo.git.config('user.email', 'somebody@everywhere.com', local=True)
        loc_repo.git.config('user.name', 'Soembody Somewhere', local=True)
        loc_repo.git.commit(message='Commit original files')
        loc_repo.git.checkout('HEAD', b='TestBranch')
        loc_repo.close()

        rem_repo_dir = env_setup.dir.parent / 'rem_repo'
        rem_repo_dir.mkdir()
        Repo.init(rem_repo_dir, bare=True)
        loc_repo.create_remote('origin', rem_repo_dir)

        pa = __main__.ParseArgs()
        pa.push_all()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert obj.repo.remotes.origin.url == loc_repo.remotes.origin.url  # assert not repo.is_dirty()
        pass

    def test_push_master(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
        monkeypatch.setattr('sys.argv', ['pytest', 'pushmaster'])
        env_setup.make_structure('loc_repo')

        loc_repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        loc_repo.git.add(all=True)
        loc_repo.git.config('user.email', 'somebody@everywhere.com', local=True)
        loc_repo.git.config('user.name', 'Soembody Somewhere', local=True)
        loc_repo.git.commit(message='Commit original files')
        # loc_repo.git.checkout('HEAD', b='TestBranch')
        loc_repo.close()

        rem_repo_dir = env_setup.dir.parent / 'rem_repo'
        rem_repo_dir.mkdir()
        Repo.init(rem_repo_dir, bare=True)
        loc_repo.create_remote('origin', rem_repo_dir)

        pa = __main__.ParseArgs()
        pa.push_master()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert obj.repo.remotes.origin.url == loc_repo.remotes.origin.url
        assert obj.repo.tags['0.0.0']
        pass


@pytest.mark.tag
class TestTag:
    def test_tag(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
        monkeypatch.setattr('sys.argv', ['pytest', 'tag', '0.0.0'])
        env_setup.make_structure()

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.git.config('user.email', 'somebody@everywhere.com', local=True)
        repo.git.config('user.name', 'Somebody Somewhere', local=True)
        repo.git.commit(message='Commit original files')
        repo.close()

        pa = __main__.ParseArgs()
        pa.tag()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert obj.repo.tags['0.0.0']
        pass

    @pytest.mark.xfail
    def test_tag_duplicate(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
        monkeypatch.setattr('sys.argv', ['pytest', 'tag', '0.0.0'])
        env_setup.make_structure()

        repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        repo.git.add(all=True)
        repo.git.commit(message='Commit original files')
        repo.close()

        pa = __main__.ParseArgs()
        pa.tag()
        args = pa.parser.parse_args()
        obj = args.func(args)
        obj = args.func(args)

        assert obj.repo.tags['0.0.0']
        pass

    @pytest.mark.parametrize(
        'tag',
        [
            # [],
            ['--release', '0.0.0'],
        ],
    )
    def test_push_tag(self, monkeypatch, env_setup_secure_self_destruct, tag):
        env_setup = env_setup_secure_self_destruct
        monkeypatch.setattr('sys.argv', ['pytest', 'pushtag'] + tag)
        env_setup.make_structure('loc_repo')
        (env_setup.dir / 'setup.cfg').write_text('[metadata]\nversion = 0.0.0')

        loc_repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        loc_repo.git.add(all=True)
        loc_repo.git.config('user.email', 'somebody@everywhere.com', local=True)
        loc_repo.git.config('user.name', 'Soembody Somewhere', local=True)
        loc_repo.git.commit(message='Commit original files')
        loc_repo.close()

        rem_repo_dir = env_setup.dir.parent / 'rem_repo'
        rem_repo_dir.mkdir()
        Repo.init(rem_repo_dir, bare=True)
        loc_repo.create_remote('origin', rem_repo_dir)

        pa = __main__.ParseArgs()
        pa.push_tag()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert obj.repo.remotes.origin.url == loc_repo.remotes.origin.url
        assert obj.repo.tags['0.0.0']
        pass

    def test_push_work(self, monkeypatch, env_setup_secure_self_destruct):
        env_setup = env_setup_secure_self_destruct
        monkeypatch.setattr('sys.argv', ['pytest', 'pushwork'])
        env_setup.make_structure('loc_repo')

        loc_repo = Repo.init(env_setup.dir, bare=False)
        os.chdir(env_setup.dir)
        loc_repo.git.add(all=True)
        loc_repo.git.config('user.email', 'somebody@everywhere.com', local=True)
        loc_repo.git.config('user.name', 'Soembody Somewhere', local=True)
        loc_repo.git.commit(message='Commit original files')
        loc_repo.git.checkout('HEAD', b='TestBranch')
        loc_repo.close()

        rem_repo_dir = env_setup.dir.parent / 'rem_repo'
        rem_repo_dir.mkdir()
        Repo.init(rem_repo_dir, bare=True)
        loc_repo.create_remote('origin', rem_repo_dir)

        pa = __main__.ParseArgs()
        pa.push_work()
        args = pa.parser.parse_args()
        obj = args.func(args)

        assert obj.repo.remotes.origin.url == loc_repo.remotes.origin.url  # assert not repo.is_dirty()
        pass
