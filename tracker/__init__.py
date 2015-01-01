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


@click.group(invoke_without_command=True)
@click.pass_context
def tracker(ctx):
    if ctx.invoked_subcommand is None:
        main()


@tracker.command()
def main():
    try:
        os.makedirs(os.path.expanduser("~/.tracker/"))
    except FileExistsError:
        pass
    with shelve.open(os.path.expanduser("~/.tracker/data")) as d:
        for item in d.items():
            click.echo(item)


@tracker.command()
@click.argument('slug')
def show(slug):
    click.echo("Hello: {}".format(slug))


if __name__ == '__main__':
    tracker()
