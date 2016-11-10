from taxcli import engine
from sqlalchemy.orm.session import sessionmaker


def get_session():
    session = sessionmaker(bind=engine)
    return session()
