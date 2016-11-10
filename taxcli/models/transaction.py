from taxcli import base

from sqlalchemy import (
    Column,
    ForeignKey,
)

from sqlalchemy.types import (
    Date,
    Integer,
    String,
)


class Transaction(base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    date = Column(Date, nullable=False)
    transaction_type = Column(String(40), ForeignKey('contacts.alias'), nullable=False)
