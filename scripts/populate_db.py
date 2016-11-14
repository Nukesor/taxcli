#!/bin/env python3
#
# This is a short script for deleting all tables/entries and creating a clean db_schema.
#
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from taxcli.models import Contact, Invoice
from taxcli.helper.postgres import get_session

session = get_session()

new_contact = Contact('test', 'Test Inc.', 'Teststr. 60',
                      'Hamburg', '22627', 'Deutschland')
new_contact.addressline2 = 'Haus 3'
new_contact.addressline3 = 'Zimmer 023'

new_invoice = Invoice('2016-1', 'test', '5000', '2016-03-05',
                      sales_tax=7, afa=0, invoice_type='income')

new_afa = Invoice('2016-2', 'test', '3600', '2016-03-05',
                  sales_tax=19, afa=3)

session.add(new_contact)
session.commit()
session.add(new_invoice)
session.add(new_afa)
session.commit()
