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

session.commit()
