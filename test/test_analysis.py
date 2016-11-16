from taxcli.models.invoice import InvoiceTypes
from taxcli.models import (
    Invoice
)


class TestInvoiceAnalysis:
    def test_invoice_creation(self, session, contact, invoice_factory):
        invoice = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .one()
        assert invoice.invoice_number == '2016-1'
        assert invoice.contact_alias == 'test'
        assert invoice.amount == 5000
        assert invoice.sales_tax == 19
        assert invoice.afa is None
        assert invoice.invoice_type == InvoiceTypes.expense
        assert invoice.date.day == 5
        assert invoice.date.month == 3
        assert invoice.date.year == 2016
        assert invoice.invoice_file is None
        assert invoice.invoice_file_type is None
