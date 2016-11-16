import os


def get_invoice_files(invoices, year=False):
    for invoice in invoices:
        if invoice.invoice_file:
            # Get folder for this invoice and create it if it doesn't exist
            if not invoice.afa:
                folder = invoice.invoice_type.name
            else:
                folder = 'afa'
            if not os.path.exists(folder):
                os.mkdir(folder)
            invoice_name = '{}-{}-{}.{}'.format(
                invoice.contact_alias,
                invoice.invoice_number,
                invoice.date.isoformat(),
                invoice.invoice_file_type,
            )

            path = os.path.join(folder, invoice_name)
            with open(path, "wb") as invoice_file:
                invoice_file.write(invoice.invoice_file)
