import enum
from taxcli import base

from sqlalchemy import (
    Column,
    CheckConstraint,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from sqlalchemy.types import (
    Boolean,
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
        ForeignKeyConstraint(['contact_alias'], ['contacts.alias'],
                             deferrable=True, initially='DEFERRED'),
        PrimaryKeyConstraint('invoice_number', 'contact_alias'),
        CheckConstraint('invoice_file is null and invoice_file_type is null or '
                        'invoice_file is not null and invoice_file_type is not null'),
        CheckConstraint('afa is not null and gwg is false or '
                        'afa is null and gwg is true or '
                        'afa is null and gwg is false')
    )

    invoice_number = Column(String(100), nullable=False)
    contact_alias = Column(String(40), nullable=False)
    amount = Column(Float(return_scale=2))
    sales_tax = Column(Integer, server_default='19')
    gwg = Column(Boolean, server_default='FALSE', nullable=False)
    afa = Column(Integer)
    pooling = Column(Boolean, server_default='FALSE', nullable=False)
    date = Column(Date, nullable=False)
    invoice_type = Column(Enum(InvoiceTypes))
    invoice_file = Column(LargeBinary)
    invoice_file_type = Column(String(10))

    def __init__(self, invoice_number, contact_alias, amount, date,
                 sales_tax=19, afa=None, pooling=False,
                 gwg=gwg, invoice_type='expense',
                 invoice_file=None, invoice_extension=None):
        self.invoice_number = invoice_number
        self.contact_alias = contact_alias
        self.amount = amount
        self.date = date
        self.sales_tax = sales_tax
        self.afa = afa
        self.pooling = pooling
        if invoice_type == 'expense':
            self.invoice_type = InvoiceTypes.expense
        else:
            self.invoice_type = InvoiceTypes.income
        self.invoice_file = invoice_file
        self.invoice_file_type = invoice_extension
