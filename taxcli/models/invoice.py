import enum
from taxcli import base

from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from sqlalchemy.types import (
    Date,
    Enum,
    Integer,
    String,
)


class InvoiceTypes(enum.Enum):
    income = 'income'
    expense = 'expense'


class Invoice(base):
    __tablename__ = 'invoices'
    __table_args__ = (
        ForeignKeyConstraint(['contact_alias'], ['contacts.alias']),
        PrimaryKeyConstraint('invoice_number', 'contact_alias'),
    )

    invoice_number = Column(String(100), nullable=False)
    contact_alias = Column(String(40), nullable=False)
    sales_tax = Column(Integer, server_default='19')
    afa = Column(Integer)
    date = Column(Date, nullable=False)
    invoice_type = Column(Enum(InvoiceTypes))
