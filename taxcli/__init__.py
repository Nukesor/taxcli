import sys
import argparse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://localhost/taxcli")
base = declarative_base(bind=engine)

import taxcli.models  # noqa

from taxcli.commands import add


def main():
    # Specifying commands
    parser = argparse.ArgumentParser(description='Taxcli')

    # Initialze supbparser
    subparsers = parser.add_subparsers(
        title='Subcommands', description='Add data or get an analysis')

    # Add
    add_types = ['transaction', 'invoice', 'contact']
    add_Subcommand = subparsers.add_parser(
        'add', help='Add data to the database')
    add_Subcommand.add_argument(
        'type', type=str, choices=add_types,
        help='The kind of data you want to add.'
    )
    add_Subcommand.add_argument(
        '--file', '-f', type=str,
        help='A file you want to attach to an invoice.'
    )
    add_Subcommand.set_defaults(func=add)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        try:
            args.func(vars(args))
        except KeyboardInterrupt:
            sys.exit(0)
