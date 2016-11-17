from terminaltables import AsciiTable


def print_invoices(invoices):
    if not isinstance(invoices, list):
        invoices = [invoices]
    invoice_data = [['Contact', 'Number', 'Amount', 'Sales tax', 'AfA', 'GwG', 'Date']]
    for invoice in invoices:
        invoice_data.append([
            invoice.contact_alias, invoice.invoice_number, invoice.amount,
            invoice.sales_tax, invoice.afa, str(invoice.gwg), invoice.date.isoformat()])
    invoice_table = AsciiTable(invoice_data)
    invoice_table.outer_border = False
    print(invoice_table.table)
