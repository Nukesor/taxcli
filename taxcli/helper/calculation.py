from sqlalchemy import extract
from taxcli.models import Invoice


def calculate_afa(invoices, year):
    afa = 0
    for invoice in invoices:
        # Every year gets the same amount
        if invoice.date.month == 1:
            if invoice.date.year >= (year-invoice.afa+1):
                afa += invoice.amount/invoice.afa
        # We have to split the costs in the middle of the start and end year
        else:
            # Start year of the invoice
            if invoice.date.year == year:
                month_amount = invoice.amount/invoice.afa/12
                afa += (12-invoice.date.month+1)*month_amount
            # End year of the invoice
            elif invoice.date.year == (year - invoice.afa):
                month_amount = invoice.amount/invoice.afa/12
                afa += (invoice.date.month-1)*month_amount
            # Years in between
            else:
                afa += invoice.amount/invoice.afa
    return afa


def calculate_netto_amount(invoices):
    amount = 0
    for invoice in invoices:
        if not invoice.afa:
            amount += invoice.amount * ((100-invoice.sales_tax)/100)
    return amount


def calculate_tax(invoices):
    tax = 0
    for invoice in invoices:
        if invoice.sales_tax:
            tax += invoice.amount * (invoice.sales_tax/100)
    return tax


def calculate_pool(session, year):
    # Tax pool invoices
    pool_invoices = session.query(Invoice) \
        .filter(extract('year', Invoice.date) >= year-5) \
        .filter(extract('year', Invoice.date) <= year) \
        .filter(Invoice.invoice_type == 'expense') \
        .filter(Invoice.gwg == False) \
        .filter(Invoice.afa == None) \
        .order_by(Invoice.date.asc()) \
        .all()

    amount = calculate_netto_amount(pool_invoices)
    return amount/5
