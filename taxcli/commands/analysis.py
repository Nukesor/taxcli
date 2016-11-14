from datetime import date
from sqlalchemy import extract
from terminaltables import AsciiTable
from taxcli.models import Invoice
from taxcli.helper.postgres import get_session


def get_month(args):
    month = int(args['month'])
    year = int(args['year'])

    session = get_session()

    # Expenses
    expenses = session.query(Invoice) \
        .filter(extract('month', Invoice.date) == month) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .order_by(Invoice.date.desc()) \
        .all()

    refund_tax = calculate_tax(expenses)

    print('Expenses: \n')
    print_invoices(expenses)

    # Income
    incomes = session.query(Invoice) \
        .filter(extract('month', Invoice.date) == month) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'income') \
        .order_by(Invoice.date.desc()) \
        .all()

    received_tax = calculate_tax(incomes)
    income_amount = calculate_amount(incomes)

    print('Incomes: \n')
    print_invoices(incomes)

    print('\n\n')
    print('Overall income'.format(income_amount))
    print('Overall sales tax to be refunded: {0:.2f}'.format(refund_tax))
    print('Overall sales tax to be pay: {0:.2f}'.format(received_tax))


def get_year(args):
    year = int(args['year'])

    session = get_session()

    expenses = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .order_by(Invoice.date.desc()) \
        .all()

    # Ust.VA + overall expense calculation
    refund_tax = calculate_tax(expenses)
    expense_amount = calculate_amount(expenses)

    print('Expenses:')
    print_invoices(expenses)

    # AfA calculation
    afa_invoices = session.query(Invoice) \
        .filter(Invoice.afa != None) \
        .filter(Invoice.invoice_type == 'expense') \
        .filter(extract('year', Invoice.date) >= (year-Invoice.afa)) \
        .order_by(Invoice.date.desc()) \
        .all()

    afa = calculate_afa(afa_invoices, year)

    print('\nAfA invoices:')
    print_invoices(expenses)

    # Income and Ust. VA income calculation
    incomes = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'income') \
        .order_by(Invoice.date.desc()) \
        .all()

    received_tax = calculate_tax(incomes)
    income_amount = calculate_amount(incomes)

    print('\nIncomes:')
    print_invoices(incomes)

    print('\n\n')
    print('Overall income: {0:.2f}'.format(income_amount))
    print('Overall expense: {0:.2f}'.format(expense_amount))

    print('Overall sales tax to be refunded: {0:.2f}'.format(refund_tax))
    print('Overall sales tax to be pay: {0:.2f}'.format(received_tax))
    print('Overall refunds from AfA: {0:.2f}'.format(afa))


def calculate_afa(invoices, year):
    afa = 0
    print('test')
    for invoice in invoices:
        # Every year gets the same amount
        if invoice.date.month != 0:
            if invoice.date.year >= (year-invoice.afa+1):
                afa += invoice.amount/invoice.afa
        # We have to split the costs in the middle of the start and end year
        else:
            # Start year of the invoice
            if invoice.date.year == year:
                mounth_amount = invoice.amount/invoice.amount/12
                afa += invoice.date.month*mounth_amount
            # End year of the invoice
            elif invoice.date.year == (year - invoice.afa):
                mounth_amount = invoice.amount/invoice.amount/12
                afa += invoice.date.month*mounth_amount
            # Years in between
            else:
                afa += invoice.amount/invoice.afa
    return afa


def calculate_amount(invoices):
    amount = 0
    for invoice in invoices:
        if not invoice.afa:
            amount += invoice.amount
    return amount


def calculate_tax(invoices):
    tax = 0
    for invoice in invoices:
        if invoice.sales_tax:
            tax += invoice.amount * (invoice.sales_tax/100)
    return tax


def print_invoices(invoices):
    invoice_data = [['Contact', 'Number', 'Amount', 'Sales tax', 'AfA', 'Date']]
    for invoice in invoices:
        invoice_data.append([
            invoice.contact_alias, invoice.invoice_number, invoice.amount,
            invoice.sales_tax, invoice.afa, invoice.date.isoformat()])
    invoice_table = AsciiTable(invoice_data)
    invoice_table.outer_border = False
    print(invoice_table.table)
