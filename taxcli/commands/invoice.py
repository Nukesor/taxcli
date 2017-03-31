import os
import sys
from datetime import datetime
from taxcli.models import Contact, Invoice, InvoiceTypes
from taxcli.helper.output import print_invoices
from taxcli.helper.postgres import get_session


def get_invoice_data(args):
    session = get_session()

    # Get file from arguments
    if args['file']:
        if not os.path.isfile(args['file']):
            print('Invalid file or file path')
            sys.exit(1)
        invoice_path = args['file']
        with open(invoice_path, "rb") as file_descriptor:
            _, extension = os.path.splitext(invoice_path)
            invoice_file = file_descriptor.read()
            extension = extension[1:]
    else:
        invoice_file = None
        extension = None

    # New Invoice
    new_invoice = Invoice(invoice_file=invoice_file, invoice_extension=extension)

    # Get an contact alias of an already existing contact
    while True:
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
            else:
                new_invoice.contact_alias = alias
                break

    # Get a invoice number
    while True:
        invoice_number = input('Invoice number:')
        if invoice_number:
            new_invoice.invoice_number = invoice_number
            break

    # Check if we already have an invoice with this number for this contact
    exists = session.query(Invoice) \
        .filter(Invoice.contact_alias == alias) \
        .filter(Invoice.invoice_number == invoice_number) \
        .one_or_none()
    if exists:
        print("There already is an invoice with this number for this contact. Aborting")
        sys.exit(1)

    # Get a date
    while True:
        date = input("Date ('YYYY-MM-DD'):")
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except:
            print('Invalid date format')
            date = None
        else:
            new_invoice.date = date
            break

    # Get invoice type
    while True:
        invoice_type = input("Invoice type (income or expense)[default: expense]:")
        invoice_type = 'expense' if invoice_type == '' else invoice_type
        if invoice_type not in ['income', 'expense']:
            print('Invalid invoice type')
            invoice_type = None
        else:
            if invoice_type == 'expense':
                new_invoice.invoice_type = InvoiceTypes.expense
                break
            else:
                new_invoice.invoice_type = InvoiceTypes.income
                break

    # Get sales tax
    while True:
        sales_tax = input("Sales tax [default: 19]:")
        sales_tax = 19 if sales_tax == '' else sales_tax
        try:
            sales_tax = int(sales_tax)
        except:
            print("Enter a valid number")
            sales_tax = None
        else:
            if sales_tax not in [0, 7, 19]:
                print("Sales tax has to be 7 or 19 percent")
            else:
                new_invoice.sales_tax = sales_tax
                break

    # Get amount
    while True:
        amount = input("Amount:")
        try:
            amount = float(amount)
        except:
            print("Not a Number.")
            amount = None
        else:
            new_invoice.amount = amount
            break

    if invoice_type == 'expense':
        netto = amount - amount*sales_tax/100
        while True:
            acquisition_invoice = input("Acquisition invoice [true, false]:")
            if acquisition_invoice.lower() == 'false':
                acquisition_invoice = False
                break
            elif acquisition_invoice.lower() == 'true':
                acquisition_invoice = True
                break
            else:
                print("Invalid input: 'true' or 'false'")

        if acquisition_invoice:
            # The amount is higher than 1000, thereby it has to be an AfA
            if netto > 1000:
                while True:
                    afa = input("Time window for AfA (years):")
                    try:
                        afa = int(afa)
                    except:
                        print("Enter a valid number or nothing")
                        afa = None
                    else:
                        new_invoice.afa = afa
                        break

            # The amount is higher than 1000, thereby it has to be an AfA
            elif netto > 150:
                new_invoice.pooling = True
            # The amount is lower than 150. Thereby we need to check manually
            # if this is supposed to be a GwG or if this should go into pooling.
            else:
                while True:
                    gwg = input("Is this a GwG [true, false]:")
                    if gwg.lower() == 'false':
                        new_invoice.pooling = True
                        break
                    elif gwg.lower() == 'true':
                        new_invoice.gwg = True
                        break
                    else:
                        print("Invalid input: 'true' or 'false'")

    session.add(new_invoice)
    session.commit()


def delete_invoice_data(args):
    session = get_session()

    alias = None
    invoice_number = None

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
        invoice_number = input('Invoice number for this alias("help" for a list):')
        if invoice_number == 'help':
            invoices = session.query(Invoice) \
                .filter(Invoice.contact_alias == alias) \
                .all()
            for invoice in invoices:
                print(invoice.invoice_number)
            invoice_number = None
        else:
            invoice = session.query(Invoice) \
                .filter(Invoice.contact_alias == alias) \
                .filter(Invoice.invoice_number == invoice_number) \
                .one_or_none()
            if not invoice:
                print("Alias doesn't exists.")
                alias = None

    session.delete(invoice)
    session.commit()


def list_invoice_data(args):
    session = get_session()

    alias = None
    invoice_number = None

    while not alias:
        alias = input('Alias for the invoices ("help" for a list):')
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

    done = False
    while not done:
        invoice_number = input('Invoice number for this alias \n'
                               '("help" for a list, leave empty for all):')
        if invoice_number == 'help':
            invoices = session.query(Invoice) \
                .filter(Invoice.contact_alias == alias) \
                .order_by(Invoice.date.desc()) \
                .all()
            print_invoices(invoices)
            invoice_number = None
        else:
            if invoice_number:
                invoices = session.query(Invoice) \
                    .filter(Invoice.contact_alias == alias) \
                    .filter(Invoice.invoice_number == invoice_number) \
                    .one_or_none()
            else:
                invoices = session.query(Invoice) \
                    .filter(Invoice.contact_alias == alias) \
                    .order_by(Invoice.date.asc()) \
                    .all()
            if not invoices:
                if invoice_number:
                    print("No such invoice_number.")
                else:
                    print("No invoices for this alias.")
                    done = False
            else:
                done = True
    print_invoices(invoices)


def add_invoice_file(args):
    session = get_session()

    if not os.path.isfile(args['file']):
        print('Invalid file or file path')
        sys.exit(1)
    invoice_path = args['file']
    with open(invoice_path, "rb") as file_descriptor:
        _, extension = os.path.splitext(invoice_path)
        invoice_file = file_descriptor.read()
        invoice_file_type = extension[1:]

    alias = None
    invoice_number = None

    while not alias:
        alias = input('Alias for the invoices ("help" for a list):')
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
        invoice_number = input('Invoice number for this alias("help" for a list):')
        if invoice_number == 'help':
            invoices = session.query(Invoice) \
                .filter(Invoice.contact_alias == alias) \
                .order_by(Invoice.date.desc()) \
                .all()
            print_invoices(invoices)
            invoice_number = None
        else:
            invoice = session.query(Invoice) \
                .filter(Invoice.contact_alias == alias) \
                .filter(Invoice.invoice_number == invoice_number) \
                .one_or_none()
            if not invoice:
                print("Alias doesn't exists.")
                alias = None

    invoice.invoice_file = invoice_file
    invoice.invoice_file_type = invoice_file_type
    session.add(invoice)
    session.commit()
