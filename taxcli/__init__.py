import sys
import argparse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://localhost/taxcli")
base = declarative_base(bind=engine)

import taxcli.models  # noqa

from taxcli.commands import add
from taxcli.commands.analysis import get_month, get_year


def main():
    # Specifying commands
    parser = argparse.ArgumentParser(description='Taxcli')

    # Initialze supbparser
    subparsers = parser.add_subparsers(
        title='Subcommands', description='Add data or get an analysis')

    # Add
    add_types = ['transaction', 'invoice', 'contact']
    add_subcommand = subparsers.add_parser(
        'add', help='Add data to the database')
    add_subcommand.add_argument(
        'type', type=str, choices=add_types,
        help='The kind of data you want to add.'
    )
    add_subcommand.add_argument(
        '--file', '-f', type=str,
        help='A file you want to attach to an invoice.'
    )
    add_subcommand.set_defaults(func=add)

    get_parser = subparsers.add_parser(
        'get', help='Get analysis of data.')

    get_subparser = get_parser.add_subparsers(
        title='`get` subcommands', description='Subcommands for getting analysis')
    month_subcommand = get_subparser.add_parser(
        'month', help='Get monthly analysis of data.')
    month_subcommand.add_argument(
        'year', type=int, help='The year you want to look at.')
    month_subcommand.add_argument(
        'month', type=int, help='The month you want to look at.')
    month_subcommand.set_defaults(func=get_month)

    year_subcommand = get_subparser.add_parser(
        'year', help='Get analysis of data for one year.')
    year_subcommand.add_argument(
        'year', type=int, help='The year you want to look at.')
    year_subcommand.set_defaults(func=get_year)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        try:
            args.func(vars(args))
        except KeyboardInterrupt:
            sys.exit(0)
