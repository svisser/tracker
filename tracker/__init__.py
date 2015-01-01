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


def get_database():
    return os.path.expanduser("~/.tracker/data")


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
    with shelve.open(get_database()) as d:
        if 'version' not in d:
            d['version'] = __version__
        if 'objects' not in d:
            d['objects'] = {}
        objects = d['objects']
        click.echo("Count: {}".format(len(objects)))


@tracker.command()
@click.argument('slug')
def show(slug):
    with shelve.open(get_database()) as d:
        objects = d['objects']
        if slug not in objects:
            click.echo("Object {} could not be found".format(slug))
            return
        click.echo("Object {}".format(slug))
        click.echo(objects[slug])


if __name__ == '__main__':
    tracker()
