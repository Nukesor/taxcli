import pytest
from taxcli.models import (
    Invoice
)

from taxcli.helper.calculation import (
    calculate_netto_amount,
    calculate_tax,
    calculate_afa,
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
        invoices = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .all()

        tax = calculate_tax(invoices)
        assert tax == 1080

    def test_afa_calculation_middle(self, session, invoice_factory):
        invoice_factory.get(
            invoice_number='2016-1',
            amount=7200,
            date='2016-04-15',
            afa=3,
        )
        invoices = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .all()

        afa = calculate_afa(invoices, 2016)
        assert afa == 1800

        afa = calculate_afa(invoices, 2017)
        assert afa == 2400

        afa = calculate_afa(invoices, 2018)
        assert afa == 2400

        afa = calculate_afa(invoices, 2019)
        assert afa == 600

    def test_afa_calculation(self, session, invoice_factory):
        invoice_factory.get(
            invoice_number='2016-1',
            amount=7200,
            date='2016-01-15',
            afa=3,
        )
        invoices = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .all()

        afa = calculate_afa(invoices, 2016)
        assert afa == 2400

        afa = calculate_afa(invoices, 2017)
        assert afa == 2400

        afa = calculate_afa(invoices, 2018)
        assert afa == 2400

    def test_multiple_afa_calculation(self, session, invoice_factory):
        invoice_factory.get(
            invoice_number='2016-1',
            amount=7200,
            date='2016-01-15',
            afa=3,
        )
        invoice_factory.get(
            invoice_number='2016-2',
            amount=7200,
            date='2016-04-15',
            afa=3,
        )
        invoices = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .all()

        afa = calculate_afa(invoices, 2016)
        assert afa == 4200

        afa = calculate_afa(invoices, 2017)
        assert afa == 4800

        afa = calculate_afa(invoices, 2018)
        assert afa == 4800

        afa = calculate_afa(invoices, 2019)
        assert afa == 600

    def test_amount_calculation(self, session, invoice_factory):
        invoice_factory.get(
            invoice_number='2016-1',
            amount=7200,
            date='2016-01-15',
        )
        invoice_factory.get(
            invoice_number='2016-2',
            amount=3200,
            date='2016-04-15',
        )
        invoices = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .all()

        amount = calculate_netto_amount(invoices)
        assert amount == 8424

    def test_dont_calculate_netto_amount_with_afa(self, session, invoice_factory):
        invoice_factory.get(
            invoice_number='2016-1',
            amount=7200,
            date='2016-01-15',
        )
        invoice_factory.get(
            invoice_number='2016-2',
            amount=3200,
            date='2016-04-15',
            afa=3,
        )
        invoices = session.query(Invoice) \
            .filter(Invoice.contact_alias == 'test') \
            .all()

        amount = calculate_netto_amount(invoices)
        assert amount == 5832
