from sqlalchemy import extract
from taxcli.models import Invoice
from taxcli.helper.postgres import get_session
from taxcli.helper.output import print_invoices
from taxcli.helper.invoice_files import get_invoice_files
from taxcli.helper.calculation import (
    calculate_afa,
    calculate_amount,
    calculate_tax,
)


def get_month(args):
    month = int(args['month'])
    year = int(args['year'])

    session = get_session()

    # Expenses
    expenses = session.query(Invoice) \
        .filter(extract('month', Invoice.date) == month) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .order_by(Invoice.date.asc()) \
        .all()

    refund_tax = calculate_tax(expenses)
    get_invoice_files(expenses)

    print('Expenses: \n')
    print_invoices(expenses)

    # Income
    incomes = session.query(Invoice) \
        .filter(extract('month', Invoice.date) == month) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'income') \
        .order_by(Invoice.date.asc()) \
        .all()

    received_tax = calculate_tax(incomes)
    income_amount = calculate_amount(incomes)
    get_invoice_files(incomes)

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
        .order_by(Invoice.date.asc()) \
        .all()

    # Ust.VA + overall expense calculation
    refund_tax = calculate_tax(expenses)
    expense_amount = calculate_amount(expenses)
    get_invoice_files(expenses)

    print('Expenses:')
    print_invoices(expenses)

    # AfA calculation
    afa_invoices = session.query(Invoice) \
        .filter(Invoice.afa != None) \
        .filter(Invoice.invoice_type == 'expense') \
        .filter(extract('year', Invoice.date) >= (year-Invoice.afa)) \
        .order_by(Invoice.date.asc()) \
        .all()

    afa = calculate_afa(afa_invoices, year)
    get_invoice_files(afa_invoices)

    print('\nAfA invoices:')
    print_invoices(afa_invoices)

    # Income and Ust. VA income calculation
    incomes = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'income') \
        .order_by(Invoice.date.asc()) \
        .all()

    received_tax = calculate_tax(incomes)
    income_amount = calculate_amount(incomes)
    get_invoice_files(incomes)

    print('\nIncomes:')
    print_invoices(incomes)

    print('\n\n')
    print('Overall income: {0:.2f}'.format(income_amount))
    print('Overall expense: {0:.2f}'.format(expense_amount))

    print('Overall sales tax to be refunded: {0:.2f}'.format(refund_tax))
    print('Overall sales tax to be pay: {0:.2f}'.format(received_tax))
    print('Overall refunds from AfA: {0:.2f}'.format(afa))
