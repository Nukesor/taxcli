from taxcli.commands.transaction import get_transaction_data
from taxcli.commands.contact import get_contact_data
from taxcli.commands.invoice import (
    get_invoice_data,
    delete_invoice_data,
    list_invoice_data,
)


def add(args):
    if args['type'] == 'transaction':
        get_transaction_data()
    elif args['type'] == 'invoice':
        get_invoice_data(args)
    elif args['type'] == 'contact':
        get_contact_data()


def delete(args):
    #if args['type'] == 'transaction':
    #    delete_transaction_data()
    if args['type'] == 'invoice':
        delete_invoice_data(args)
    #elif args['type'] == 'contact':
    #    delete_contact_data()


def lists(args):
    #if args['type'] == 'transaction':
    #    list_transaction_data()
    if args['type'] == 'invoice':
        list_invoice_data(args)
    #elif args['type'] == 'contact':
    #    list_contact_data()
