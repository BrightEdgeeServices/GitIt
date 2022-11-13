import argparse
import sys
from gitit.setenv import setenv
from gitit.add import add
from gitit.commit import commit


class ParseArgs:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='gitit',
            description='Facilitate the standardization of git commands in a project',
        )
        self.subparsers = self.parser.add_subparsers(title='Commands')
        self.parser_add_a = None
        self.parser_commit_def = None
        self.parser_commit_msg = None
        self.parser_commit_pre = None
        self.parser_setenv = None

    def setenv(self):
        self.parser_setenv = self.subparsers.add_parser(
            'setenv',
            help='Set the environment variables for the project.',
            # aliases=['se']
        )
        self.parser_setenv.add_argument('--py-version', help='Installed python version')
        self.parser_setenv.add_argument('--issue-prefix', help='Prefix for git issues')
        self.parser_setenv.add_argument('--project-name', help='Project name')
        self.parser_setenv.set_defaults(func=setenv.Environment)
        pass

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
            help='Commit a branch with the default message.',
        )
        self.parser_commit_pre.add_argument(
            '-m',
            '--msg',
            help='Commit a branch with a pre defined message.',
        )
        self.parser_commit_pre.set_defaults(func=commit.CommitPre)
        pass


def main():
    pa = ParseArgs()
    pa.setenv()
    pa.add_a()
    pa.commit_def()
    pa.commit_cust()
    pa.commit_pre()
    if len(sys.argv) > 1:
        # import pdb;pdb.set_trace()
        args = pa.parser.parse_args()
        args.func(args)
    else:
        pa.parser.print_help()
        sys.exit(2)
    pass


if __name__ == "__main__":
    main()
