import os

from taxcli.models.invoice import InvoiceTypes
from taxcli.models import (
    Invoice
)


class TestInvoiceAnalysis:
    def test_invoice(self, session, invoice_factory):
        invoice_factory.get()
        invoice = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .one()
        assert invoice.invoice_number == '2016-1'
        assert invoice.contact_alias == 'test'
        assert invoice.amount == 5000
        assert invoice.sales_tax == 19
        assert invoice.afa is None
        assert invoice.gwg is None
        assert invoice.invoice_type == InvoiceTypes.expense
        assert invoice.date.day == 5
        assert invoice.date.month == 3
        assert invoice.date.year == 2016
        assert invoice.invoice_file is None
        assert invoice.invoice_file_type is None

    def test_invoice_factory(self, session, invoice_factory):
        invoice_path = os.path.join('test', 'media', 'test.pdf')
        with open(invoice_path, 'rb') as pdf_file:
            _, extension = os.path.splitext(invoice_path)
            invoice_file = pdf_file.read()
            invoice_file_type = extension

        invoice_factory.get(invoice_number='2016-2', contact_alias='test',
                            amount='10000', date='2016-05-05',
                            sales_tax=7, invoice_type='income',
                            invoice_file=invoice_file, invoice_extension=invoice_file_type)
        invoice = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .one()
        assert invoice.invoice_number == '2016-2'
        assert invoice.contact_alias == 'test'
        assert invoice.amount == 10000
        assert invoice.sales_tax == 7
        assert invoice.afa == 0
        assert invoice.gwg is None
        assert invoice.invoice_type == InvoiceTypes.income
        assert invoice.date.day == 5
        assert invoice.date.month == 5
        assert invoice.date.year == 2016
