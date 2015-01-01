# -*- coding: utf-8 -*-

__title__ = 'tracker'
__version__ = '0.0.1'
__author__ = 'Simeon Visser'
__email__ = 'simeonvisser@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Simeon Visser'

import click


@click.command()
def main():
    click.echo("Hello")


if __name__ == '__main__':
    main()
