from sqlalchemy import extract
from terminaltables import AsciiTable
from taxcli.models import Contact, Invoice
from taxcli.helper.postgres import get_session


def get_month(args, return=False):
    month = int(args['month'])
    year = int(args['year'])

    session = get_session()

    refund_tax = 0
    received_tax = 0

    expenses = session.query(Invoice) \
        .filter(extract('month', Invoice.date) == month) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .order_by(Invoice.date.desc()) \
        .all()

    expense_data = [['Contact', 'Number', 'Amount', 'Sales tax', 'AfA', 'Date']]
    for expense in expenses:
        if expense.sales_tax:
            refund_tax += expense.amount * (expense.sales_tax/100)
        expense_data.append([
            expense.contact_alias, expense.invoice_number, expense.amount,
            expense.sales_tax, expense.afa, expense.date.isoformat()])

    print('Expenses: \n')
    expense_table = AsciiTable(expense_data)
    expense_table.outer_border = False
    print(expense_table.table)

    incomes = session.query(Invoice) \
        .filter(extract('month', Invoice.date) == month) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'income') \
        .order_by(Invoice.date.desc()) \
        .all()

    income_data = [['Contact', 'Number', 'Amount', 'Sales tax', 'AfA', 'Date']]
    for income in incomes:
        if income.sales_tax:
            refund_tax += income.amount * (income.sales_tax/100)
        income_data.append([
            income.contact_alias, income.invoice_number, income.amount,
            income.sales_tax, income.afa, income.date.isoformat()])

    if return:
        return refund_tax, received_tax
    else:
        print('\n\n')
        print('Overall sales tax to be refunded: {0:.2f}'.format(refund_tax))
        print('Overall sales tax to be pay: {0:.2f}'.format(received_tax))


def get_year(args):
    year = int(args['year'])

    refunds = 0
    afa_refunds = 0
    refund_tax = 0
    received_tax = 0

    expenses = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .order_by(Invoice.date.desc()) \
        .all()

    # Ust.VA + overall expense calculation
    expense_data = [['Contact', 'Number', 'Amount', 'Sales tax', 'AfA', 'Date']]
    for expense in expenses:
        if expense.sales_tax:
            refund_tax += expense.amount * (expense.sales_tax/100)
        expense_data.append([
            expense.contact_alias, expense.invoice_number, expense.amount,
            expense.sales_tax, expense.afa, expense.date.isoformat()])
        if not expense.afa:
            refunds += expense.amount

    print('Expenses: \n')
    expense_table = AsciiTable(expense_data)
    expense_table.outer_border = False
    print(expense_table.table)


    # AfA calculation
    expenses = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'expense') \
        .order_by(Invoice.date.desc()) \
        .all()

    expense_data = [['Contact', 'Number', 'Amount', 'Sales tax', 'AfA', 'Date']]
    for expense in expenses:
        if expense.sales_tax:
            refund_tax += expense.amount * (expense.sales_tax/100)
        expense_data.append([
            expense.contact_alias, expense.invoice_number, expense.amount,
            expense.sales_tax, expense.afa, expense.date.isoformat()])
        if not expense.afa:
            refunds += expense.amount

    print('Expenses: \n')
    expense_table = AsciiTable(expense_data)
    expense_table.outer_border = False
    print(expense_table.table)

    # Income and Ust. VA income calculation
    incomes = session.query(Invoice) \
        .filter(extract('year', Invoice.date) == year) \
        .filter(Invoice.invoice_type == 'income') \
        .order_by(Invoice.date.desc()) \
        .all()

    income_data = [['Contact', 'Number', 'Amount', 'Sales tax', 'AfA', 'Date']]
    for income in incomes:
        if income.sales_tax:
            refund_tax += income.amount * (income.sales_tax/100)
        income_data.append([
            income.contact_alias, income.invoice_number, income.amount,
            income.sales_tax, income.afa, income.date.isoformat()])

    if return:
        return refund_tax, received_tax
    else:
        print('\n\n')
        print('Overall sales tax to be refunded: {0:.2f}'.format(refund_tax))
        print('Overall sales tax to be pay: {0:.2f}'.format(received_tax))
        print('Overall refunds from AfA: {0:.2f}'.format(afa))


def get_afa_for_year(args)
