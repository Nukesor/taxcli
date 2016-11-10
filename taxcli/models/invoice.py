import enum
from taxcli import base

from sqlalchemy import (
    Column,
    CheckConstraint,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from sqlalchemy.types import (
    Date,
    Enum,
    Integer,
    LargeBinary,
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
        CheckConstraint('invoice_file is null and invoice_file_type is null or '
                        'invoice_file is not null and invoice_file_type is not null'),
    )

    invoice_number = Column(String(100), nullable=False)
    contact_alias = Column(String(40), nullable=False)
    sales_tax = Column(Integer, server_default='19')
    afa = Column(Integer)
    date = Column(Date, nullable=False)
    invoice_type = Column(Enum(InvoiceTypes))
    invoice_file = Column(LargeBinary)
    invoice_file_type = Column(String(10))
