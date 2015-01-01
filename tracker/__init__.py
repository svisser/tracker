# -*- coding: utf-8 -*-

__title__ = 'tracker'
__version__ = '0.0.1'
__author__ = 'Simeon Visser'
__email__ = 'simeonvisser@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Simeon Visser'

import os
import shelve

import click


@click.command()
def main():
    try:
        os.makedirs(os.path.expanduser("~/.tracker/"))
    except FileExistsError:
        pass
    with shelve.open(os.path.expanduser("~/.tracker/data")) as d:
        for item in d.items():
            click.echo(item)


if __name__ == '__main__':
    main()
