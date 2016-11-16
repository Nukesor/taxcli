import pytest
import taxcli.helper.postgres

from taxcli import engine
from taxcli.helper.postgres import get_session
from taxcli.models import (
    Contact,
    Invoice,
    Transaction,
)


@pytest.fixture(scope='function')
def dbtransaction(request):
    """Temporary DB transaction.

    Use this if you want to operate on the real database but don't want changes to actually affect
    it outside of this test. This works using SQLAlchemy transactions.

    Transactions made outside of the session scope are not rolled back.
    """
    connection = engine.connect()
    transaction = connection.begin()

    def teardown():
        # Explicitly remove the session so that we'll get a new session every time we go here.

        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture(scope='function')
def session(request, dbtransaction, monkeypatch):
    """Mock the get_session function used for all sessions in taxcli."""
    session = get_session(connection=dbtransaction)
    monkeypatch.setattr(taxcli.helper.postgres, 'get_session', lambda *args: session)

    return session


@pytest.fixture()
def invoice_factory(session):
    """Returns a class for generating Invoices."""
    class InvoiceFactory():
        def get(self, invoice_number='2016-1', contact_alias='test',
                amount='5000', date='2016-03-05',
                sales_tax=19, afa=None,
                invoice_type='expense', invoice_path=None):
            """Return an Invoice."""
            invoice = Invoice(
                invoice_number, contact_alias, amount, date,
                sales_tax=19, afa=None, invoice_type='expense', invoice_path=None)
            session.add(invoice)
            session.commit()
            return invoice
    return InvoiceFactory()


@pytest.fixture(scope='function')
def contact_factory(session):
    """Returns a class for generating Invoices."""
    class InvoiceFactory():
        def get(self, alias='Test', name='Test Inc.',
                addressline1='Teststr. 60',
                addressline2=None,
                addressline3=None,
                city='Hamburg', zip_or_post='22627',
                state_province_county=None,
                country='Deutschland'):
            """Return an Invoice."""
            contact = Contact(alias, name, addressline1, city, zip_or_post, country)
            contact.addressline2 = None
            contact.addressline3 = None
            session.add(contact)
            session.commit()
            return contact
    return Contact()


@pytest.fixture(scope='function')
def contact(session, invoice_factory):
    """Returns a default test contact."""
    invoice_factory.get()
