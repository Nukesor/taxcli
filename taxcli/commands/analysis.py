from sqlalchemy import extract
from taxcli.models import Invoice
from taxcli.helper.postgres import get_session
from taxcli.helper.output import print_invoices
from taxcli.helper.invoice_files import get_invoice_files
from taxcli.helper.calculation import (
    calculate_afa,
    calculate_netto_amount,
    calculate_pool,
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
    income_amount = calculate_netto_amount(incomes)
    get_invoice_files(incomes)

    print('Incomes: \n')
    print_invoices(incomes)

    print('\n\n')
    print('Overall income: {}'.format(income_amount))
    print('Overall sales tax to be refunded: {0:.2f}'.format(refund_tax))
    print('Overall sales tax to be payed: {0:.2f}'.format(received_tax))


def get_year(args):
    year = int(args['year'])

    session = get_session()

    # Regular expenses
    expense_invoices = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .filter(Invoice.gwg == False) \
        .filter(Invoice.afa == None) \
        .filter(Invoice.pooling == False) \
        .order_by(Invoice.date.asc()) \
        .all()  # NOQA

    # Ust.VA + overall expense calculation
    refund_tax = calculate_tax(expense_invoices)
    expense_amount = calculate_netto_amount(expense_invoices)
    get_invoice_files(expense_invoices)

    print('Expenses (Services of other companies):')
    print_invoices(expense_invoices)

    # GwG invoices
    gwg_invoices = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .filter(Invoice.gwg == True) \
        .order_by(Invoice.date.asc()) \
        .all()  # NOQA

    # Ust.VA + overall expense calculation
    refund_tax += calculate_tax(gwg_invoices)
    gwg_amount = calculate_netto_amount(gwg_invoices)
    get_invoice_files(gwg_invoices)

    print('\nGwG:')
    print_invoices(gwg_invoices)

    # Tax pool invoices
    pool_invoices = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .filter(Invoice.pooling == True) \
        .order_by(Invoice.date.asc()) \
        .all()  # NOQA

    # Ust.VA + overall expense calculation
    refund_tax += calculate_tax(pool_invoices)
    pool_amount = calculate_pool(session, 2016)
    get_invoice_files(pool_invoices)

    print('\nPool invoices:')
    print_invoices(pool_invoices)

    # AfA calculation
    afa_invoices = session.query(Invoice) \
        .filter(Invoice.afa != None) \
        .filter(Invoice.invoice_type == 'expense') \
        .filter(extract('year', Invoice.date) >= (year-Invoice.afa)) \
        .order_by(Invoice.date.asc()) \
        .all()  # NOQA

    refund_tax += calculate_tax(afa_invoices)
    afa_amount = calculate_afa(afa_invoices, year)
    get_invoice_files(afa_invoices)

    print('\nAfA:')
    print_invoices(afa_invoices)

    # Income and Ust. VA income calculation
    incomes = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'income') \
        .order_by(Invoice.date.asc()) \
        .all()

    received_tax = calculate_tax(incomes)
    income_amount = calculate_netto_amount(incomes)
    get_invoice_files(incomes)

    print('\nIncomes:')
    print_invoices(incomes)

    print('\n\n')
    print('Overall income: {0:.2f}'.format(income_amount))
    print('Overall expense: {0:.2f}'.format(expense_amount))

    print('\nExpense refunds: {0:.2f}'.format(expense_amount))
    print('Gwg refunds: {0:.2f}'.format(gwg_amount))
    print('Pool refunds: {0:.2f}'.format(pool_amount))
    print('Afa refunds: {0:.2f}'.format(afa_amount))

    print('\nOverall sales tax to be refunded: {0:.2f}'.format(refund_tax))
    print('Overall sales tax to pay: {0:.2f}'.format(received_tax))
