import pytest
from taxcli.models import (
    Invoice
)

from taxcli.helper.calculation import (
    calculate_tax,
)


class TestInvoiceCalculation:
    @pytest.mark.parametrize('tax, result', [(7, 140), (19, 380)])
    def test_tax_calculation_19(self, session, invoice_factory, tax, result):
        invoice_factory.get(
            amount=2000,
            sales_tax=tax,
        )
        invoice = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .filter(Invoice.invoice_number == '2016-1') \
            .one()

        tax = calculate_tax([invoice])
        assert tax == result

    def test_tax_calculation(self, session, invoice_factory):
        invoice_factory.get(
            invoice_number='2016-1',
            amount=2000,
            sales_tax=19,
        )
        invoice_factory.get(
            invoice_number='2016-2',
            amount=2000,
            sales_tax=7,
        )
        invoice_factory.get(
            invoice_number='2016-3',
            amount=8000,
            sales_tax=7,
        )
        invoice = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .all()

        tax = calculate_tax(invoice)
        assert tax == 1080
