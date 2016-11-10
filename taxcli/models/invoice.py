import os
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
    Float,
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
    amount = Column(Float(return_scale=2))
    sales_tax = Column(Integer, server_default='19')
    afa = Column(Integer)
    date = Column(Date, nullable=False)
    invoice_type = Column(Enum(InvoiceTypes))
    invoice_file = Column(LargeBinary)
    invoice_file_type = Column(String(10))

    def __init__(self, invoice_number, contact_alias, amount, date,
                 sales_tax=19, afa=None, invoice_type='expense', invoice_path=None):
        self.invoice_number = invoice_number
        self.contact_alias = contact_alias
        self.amount = amount
        self.date = date
        self.sales_tax = sales_tax
        self.afa = afa
        if invoice_type == 'expense':
            self.invoice_type = InvoiceTypes.expense
        else:
            self.invoice_type = InvoiceTypes.income
        if invoice_path:
            with open(invoice_path, "rb") as file_descriptor:
                _, extension = os.path.splitext(invoice_path)
                data = file_descriptor.read()
                self.invoice_file = data
                self.invoice_file_type = extension
