from taxcli import base

from sqlalchemy import (
    Column,
)

from sqlalchemy import (
    String,
)


class Contact(base):
    __tablename__ = 'contacts'

    alias = Column(String(40), primary_key=True)
    name = Column(String(100), nullable=False)
    addressline1 = Column(String(60), nullable=False)
    addressline2 = Column(String(60))
    addressline3 = Column(String(60))
    city = Column(String(60), nullable=False)
    zip_or_postcode = Column(String(10), nullable=False)
    state_province_county = Column(String(60))
    country = Column(String(60), nullable=False)

    def __init__(self, alias, name, addressline1, city, zip_or_postcode, country):
        self.alias = alias
        self.name = name
        self.addressline1 = addressline1
        self.city = city
        self.zip_or_postcode = zip_or_postcode
        self.country = country
