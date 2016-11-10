from taxcli import base

from sqlalchemy import Column

from sqlalchemy.types import (
    Date,
    Integer,
    String,
)


class Transaction(base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    transaction_type = Column(String(40))

    def __init__(self, amount, date, transaction_type=None):
        self.amount = amount
        self.date = date
        self.transaction_type = transaction_type
