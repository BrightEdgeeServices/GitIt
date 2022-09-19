'''Project Short Description (default ini)

Project long description or extended summary goes in here (default ini)
'''

import logging
from pathlib import Path
from termcolor import colored
from beetools import beearchiver, beeutils

_PROJ_DESC = __doc__.split('\n')[0]
_PROJ_PATH = Path(__file__)


def project_desc():
    return _PROJ_DESC


class gitit:
    '''Class short description one-liner goes here.

    Class multi-liner detail description goes here.
    '''

    def __init__(self, p_project_name, p_dir, p_parent_log_name='', p_verbose=True):
        '''Initialize the class

        Parameters
        ----------
        p_parent_log_name : str
            Name of the parent.  In combination witt he class name it will
            form the logger name.
        p_logger : bool, default = False
            Activate the logger
        p_verbose: bool, default = True
            Write messages to the console.

        Returns
        -------

        See Also
        --------

        Notes
        -----

        Examples
        --------
        '''
        self.success = True
        if p_parent_log_name:
            self.log_name = '{}.{}'.format(p_parent_log_name, gitit)
            self.logger = logging.getLogger(self._log_name)
        self.project_name = p_project_name
        self.dir = p_dir
        self.verbose = p_verbose

    def method_1(self, p_msg):
        '''Method short description one-liner goes here.

        Class multi-liner detail description goes here.

        Parameters
        ----------

        Returns
        -------

        See Also
        --------

        Notes
        -----

        Examples
        --------

        '''
        print(colored('Testing {}...'.format(self.project_name), 'yellow'))
        print(colored('Message: {}'.format(p_msg), 'yellow'))
        return True


def do_examples(p_cls=True):
    '''A collection of implementation examples for gitit.

    A collection of implementation examples for gitit. The examples
    illustrate in a practical manner how to use the methods.  Each example
    show a different concept or implementation.

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the examples.

    See Also
    --------

    Notes
    -----

    Examples
    --------

    '''
    success = do_example1(p_cls)
    success = do_example2(False) and success
    return success


def do_example1(p_cls=True):
    '''A working example of the implementation of gitit.

    Example1 illustrate the following concepts:
    1. Bla, bla, bla
    2. Bla, bla, bla

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the example

    See Also
    --------

    Notes
    -----

    Examples
    --------

    '''
    success = True
    archiver = beearchiver.Archiver(_PROJ_DESC, _PROJ_PATH)
    archiver.print_header(p_cls=p_cls)
    t_dir = beeutils.get_tmp_dir()
    t_gitit = gitit("gitit", t_dir)
    t_gitit.method_1('This is do_example1')
    beeutils.rm_tree(t_dir)
    archiver.print_footer()
    return success


def do_example2(p_cls=True):
    '''Another working example of the implementation of gitit.

    Example2 illustrate the following concepts:
    1. Bla, bla, bla
    2. Bla, bla, bla

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the method

    See Also
    --------

    Notes
    -----

    Examples
    --------

    '''
    success = True
    archiver = beearchiver.Archiver(_PROJ_DESC, _PROJ_PATH)
    archiver.print_header(p_cls=p_cls)
    t_dir = beeutils.get_tmp_dir()
    t_gitit = gitit("gitit", t_dir)
    t_gitit.method_1('This is do_example2')
    beeutils.rm_tree(t_dir)
    archiver.print_footer()
    return success


if __name__ == '__main__':
    do_examples()
