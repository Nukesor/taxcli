from taxcli.commands.transaction import get_transaction_data
from taxcli.commands.contact import get_contact_data
from taxcli.commands.invoice import get_invoice_data


def add(args):
    if args['type'] == 'transaction':
        get_transaction_data()
    elif args['type'] == 'invoice':
        get_invoice_data(args)
    elif args['type'] == 'contact':
        get_contact_data()
