# -*- coding: utf-8 -*-

__title__ = 'tracker'
__version__ = '0.0.1'
__author__ = 'Simeon Visser'
__email__ = 'simeonvisser@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Simeon Visser'

import contextlib
import datetime
import os
import shelve

import click


@contextlib.contextmanager
def get_database():
    with shelve.open(os.path.expanduser("~/.tracker/data"),
                     writeback=True) as data:
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


@tracker.command(help="Display overview of all objects")
def main():
    try:
        os.makedirs(os.path.expanduser("~/.tracker/"))
    except FileExistsError:
        pass
    with get_database() as data:
        objects = data['objects']
        click.echo("Count: {}".format(len(objects)))


@tracker.command(help="Display details of an object")
@click.argument('slug')
def show(slug):
    skipped_facts = set(('name',))
    with get_database() as data:
        objects = data['objects']
        if slug not in objects:
            click.echo("Object {} could not be found".format(slug))
            return
        display_name = slug
        if objects[slug]['facts'].get('name'):
            display_name = objects[slug]['facts']['name']
        click.echo("{} - Updated: {} - Created: {}".format(
            display_name,
            objects[slug]['timestamp_updated'].strftime("%B %d, %Y"),
            objects[slug]['timestamp_created'].strftime("%B %d, %Y"),
        ))
        if objects[slug]['facts']:
            click.echo("Facts:")
            for key, value in sorted(objects[slug]['facts'].items()):
                if key in skipped_facts:
                    continue
                click.echo('- ({}) - {}: {}'.format(
                    value['timestamp_updated'].strftime("%B %d, %Y"),
                    key,
                    value['value']))


@tracker.command(help="Add an object to the database")
@click.argument('slug')
def add(slug):
    with get_database() as data:
        if slug in data['objects']:
            raise click.ClickException(
                "Object {} already in database".format(slug))
        utcnow = datetime.datetime.utcnow()
        data['objects'][slug] = {
            'timestamp_created': utcnow,
            'timestamp_updated': utcnow,
            'facts': {},
        }


@tracker.command(help="Rename the object identifier for an object")
@click.argument('old_slug')
@click.argument('new_slug')
def move(old_slug, new_slug):
    with get_database() as data:
        if old_slug not in data['objects']:
            raise click.ClickExceptioN(
                "Object {} not found in database".format(slug))
        obj = data['objects'][old_slug]
        data['objects'][new_slug] = obj
        del data['objects'][old_slug]


@tracker.command(help="Store a fact for an object")
@click.argument('slug')
@click.argument('fact')
@click.argument('value')
def fact(slug, fact, value):
    with get_database() as data:
        if slug not in data['objects']:
            raise click.ClickException(
                "Object {} not found in database".format(slug))
        utcnow = datetime.datetime.utcnow()
        obj = data['objects'][slug]
        obj['timestamp_updated'] = utcnow
        obj['facts'][fact] = {
            'timestamp_updated': utcnow,
            'value': value,
        }


if __name__ == '__main__':
    tracker()
