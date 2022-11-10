import argparse
from gitit.setenv import setenv
from gitit.add import adda


class ParseArgs:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='gitit',
            description='Facilitate the standardization of git commands in a project',
        )
        self.subparsers = self.parser.add_subparsers(title='Commands')
        self.parser_adda = None
        self.parser_setenv = None

    def setenv(self):
        self.parser_setenv = self.subparsers.add_parser(
            'setenv',
            help='Set the environment variables for the project.',
            # aliases=['se']
        )
        self.parser_setenv.add_argument(
            '--py-version', help='Installed python version'
        )
        self.parser_setenv.add_argument('--issue-prefix', help='Prefix for git issues')
        self.parser_setenv.add_argument('--project-name', help='Project name')
        self.parser_setenv.set_defaults(func= setenv.Environment)
        pass

    def adda(self):
        self.parser_adda = self.subparsers.add_parser(
            'adda',
            help='This adds, modifies, and removes index entries to match the working tree.',
            # aliases=['aa']
        )
        self.parser_adda.add_argument('--all', help='Add all files')
        self.parser_adda.set_defaults(func= adda.AddA)
        pass


def main():
    pa = ParseArgs()
    pa.setenv()
    pa.adda()
    args = pa.parser.parse_args()
    # print(f"Args: {args}")
    # try:
    args.func(args)
    # except:
    #     # pa.parser.print_help()
    #     sys.exit(2)
    pass


if __name__ == "__main__":
    # import pdb;pdb.set_trace()
    main()
