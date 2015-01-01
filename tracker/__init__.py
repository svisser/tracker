# -*- coding: utf-8 -*-

__title__ = 'tracker'
__version__ = '0.0.1'
__author__ = 'Simeon Visser'
__email__ = 'simeonvisser@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Simeon Visser'

import contextlib
import os
import shelve

import click


@contextlib.contextmanager
def get_database():
    with shelve.open(os.path.expanduser("~/.tracker/data"), writeback=True) as data:
        if not data:
            data['version'] = __version__
        if 'objects' not in data:
            data['objects'] = {}
        if 'version' not in data:
            raise click.ClickException("Unknown version for database")
        yield data


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
    with get_database() as data:
        objects = data['objects']
        click.echo("Count: {}".format(len(objects)))


@tracker.command()
@click.argument('slug')
def show(slug):
    with get_database() as data:
        objects = data['objects']
        if slug not in objects:
            click.echo("Object {} could not be found".format(slug))
            return
        click.echo("Object {}".format(slug))
        click.echo(objects[slug])


@tracker.command()
@click.argument('slug')
def add(slug):
    with get_database() as data:
        if slug in data['objects']:
            raise click.ClickException("Object {} already in database".format(slug))
        data['objects'][slug] = {
            'facts': {},
        }


if __name__ == '__main__':
    tracker()
