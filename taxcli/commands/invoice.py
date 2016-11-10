import os
import sys
from datetime import datetime
from taxcli.models import Contact, Invoice
from taxcli.helper.postgres import get_session


def get_invoice_data(args):
    session = get_session()

    if args['file']:
        if not os.path.isfile(args['file']):
            print('Invalid file or file path')
            sys.exit(1)
        invoice_path = args['file']
    else:
        invoice_path = None

    alias = None
    invoice_number = None
    amount = None
    invoice_type = None
    date = None
    sales_tax = None
    afa = None

    while not alias:
        alias = input('Alias for this invoice ("help" for a list):')
        if alias == 'help':
            contacts = session.query(Contact).all()
            for contact in contacts:
                print(contact.alias)
            alias = None
        else:
            exists = session.query(Contact).get(alias)
            if not exists:
                print("Alias doesn't exists.")
                alias = None

    while not invoice_number:
        invoice_number = input('Invoice number:')

    # Check if we already have an invoice with this number for this contact
    exists = session.query(Invoice) \
        .filter(Invoice.contact_alias == alias) \
        .filter(Invoice.invoice_number == invoice_number) \
        .one_or_none()
    if exists:
        print("There already is an invoice with this number for this contact. Aborting")
        sys.exit(1)

    while not amount:
        amount = input("Money amount:")
        try:
            amount = float(amount)
        except:
            print("Not a Number.")
            amount = None

    while not date:
        date = input("Date ('YYYY-MM-DD'):")
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except:
            print('Invalid date format')
            date = None

    while not invoice_type:
        invoice_type = input("Invoice type (income or expense)[expense]:")
        invoice_type = 'expense' if invoice_type == '' else invoice_type
        if invoice_type not in ['income', 'expense']:
            print('Invalid invoice type')
            invoice_type = None

    while not sales_tax:
        sales_tax = input("Sales tax [19]:")
        sales_tax = 19 if sales_tax == '' else sales_tax
        try:
            sales_tax = int(sales_tax)
        except:
            print("Enter a valid number")
            sales_tax = None
        if sales_tax not in [7, 19]:
            print("Sales tax has to be 7 or 19 percent")

    while afa is None:
        afa = input("Time window for afa (years):")
        if afa != '':
            try:
                afa = int(afa)
            except:
                print("Enter a valid number or nothing")
                afa = None
    afa = None if afa == '' else afa

    new_invoice = Invoice(invoice_number, alias, amount, date,
                          sales_tax=sales_tax, afa=afa, invoice_type=invoice_type,
                          invoice_path=invoice_path)

    session.add(new_invoice)
    session.commit()
