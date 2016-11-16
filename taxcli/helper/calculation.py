def calculate_afa(invoices, year):
    afa = 0
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


