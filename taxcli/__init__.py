from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://localhost/taxcli", echo=True)
base = declarative_base(bind=engine)

import taxcli.models
