import argparse
import sys
from gitit.add import add
from gitit.branch import branch
from gitit.commit import commit
from gitit.push import push
from gitit.tag import tag


class ParseArgs:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='gitit',
            description='Facilitate the standardization of git commands in a project',
        )
        self.branch_new_group = None
        self.parser_add_a = None
        self.parser_branch_new = None
        self.parser_commit_def = None
        self.parser_commit_cust = None
        self.parser_commit_pre = None
        self.parser_push = None
        self.parser_push_tag = None
        self.subparsers = self.parser.add_subparsers(title='Commands')

    def add_a(self):
        self.parser_add_a = self.subparsers.add_parser(
            'adda',
            help='Mimic the "git add -A" command.  Only explicitly allow adding to "main" or "master".',
        )
        self.parser_add_a.add_argument(
            '-m',
            '--master',
            action='store_true',
            default=False,
            help='Enable add to "master or "main" branches',
        )
        self.parser_add_a.set_defaults(func=add.AddA)
        pass

    def branch_new(self):
        self.parser_branch_new = self.subparsers.add_parser(
            'branchnew',
            help='Create a new branch from the current or master branch.',
        )
        self.branch_new_group = self.parser_branch_new.add_mutually_exclusive_group()
        self.branch_new_group.add_argument(
            '-m',
            '--master-branch',
            action='store_true',
            default=True,
            help='Make the master branch the source for the new branch',
        )
        self.branch_new_group.add_argument(
            '-b',
            '--current-branch',
            action='store_false',
            default=False,
            help='Make the current branch the source for the new branch',
        )
        self.parser_branch_new.add_argument(
            '-c',
            '--category',
            choices=['bugfix', 'feature', 'hotfix'],
            default='feature',
            help='Category prefix',
        )
        self.parser_branch_new.add_argument(
            '-i',
            '--issue',
            type=int,
            required=True,
            help='Issue number in GitHub',
        )
        self.parser_branch_new.add_argument(
            '-d',
            '--desc',
            required=True,
            help='Short description of the branch less than 20 characters',
        )
        self.parser_branch_new.add_argument(
            '-s',
            '--stash',
            action='store_true',
            default='True',
            help='Stash files in a dirty repository.',
        )
        self.parser_branch_new.set_defaults(func=branch.BranchNew)
        pass

    def commit_def(self):
        self.parser_commit_def = self.subparsers.add_parser(
            'commitdef',
            help='Commit branch with the default message.',
        )
        self.parser_commit_def.set_defaults(func=commit.CommitDef)
        pass

    def commit_cust(self):
        self.parser_commit_cust = self.subparsers.add_parser(
            'commitcust',
            help='Commit branch with a custom message.',
        )
        self.parser_commit_cust.add_argument(
            '-m',
            '--msg',
            help='Custom message for the commit.',
        )
        self.parser_commit_cust.set_defaults(func=commit.CommitCust)
        pass

    def commit_pre(self):
        self.parser_commit_pre = self.subparsers.add_parser(
            'commitpre',
            help='Commit a branch with a predefined message.',
        )
        self.parser_commit_pre.add_argument(
            'msg',
            choices=commit.CommitMsgs().dict().keys(),
            help='Commit a branch with a pre defined message.',
        )
        self.parser_commit_pre.set_defaults(func=commit.CommitPre)
        pass

    def push_all(self):
        self.parser_push = self.subparsers.add_parser(
            'pushall',
            help='Push master branch to the remote repository.',
        )
        self.parser_push.set_defaults(func=push.PushAll)
        pass

    def push_master(self):
        self.parser_push = self.subparsers.add_parser(
            'pushmaster',
            help='Push master branch to the remote repository.',
        )
        self.parser_push.set_defaults(func=push.PushMaster)
        pass

    def push_tag(self):
        self.parser_push_tag = self.subparsers.add_parser(
            'pushtag',
            help='Tag a branch and push it to the remote repository.',
        )
        self.parser_push_tag.add_argument(
            '--release',
            default=None,
            help='Add a tag in the semantic version format (major.minor.patch).',
        )
        self.parser_push_tag.set_defaults(func=push.PushTag)
        pass

    def push_work(self):
        self.parser_push = self.subparsers.add_parser(
            'pushwork',
            help='Push branch to the remote repository.',
        )
        self.parser_push.set_defaults(func=push.PushWork)
        pass

    def tag(self):
        self.parser_tag = self.subparsers.add_parser(
            'tag',
            help='Tag a branch.',
        )
        self.parser_tag.add_argument(
            'release',
            help='Symantic release.',
        )
        self.parser_tag.set_defaults(func=tag.Tag)
        pass


def main():
    pa = ParseArgs()
    pa.add_a()
    pa.branch_new()
    pa.commit_def()
    pa.commit_cust()
    pa.commit_pre()
    pa.push_all()
    pa.push_master()
    pa.push_tag()
    pa.push_work()
    pa.tag()
    if len(sys.argv) > 1:
        args = pa.parser.parse_args()
        args.func(args)
    else:
        pa.parser.print_help()
        sys.exit(2)
    pass


if __name__ == "__main__":
    main()
