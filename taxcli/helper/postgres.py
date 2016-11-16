from taxcli import engine
from sqlalchemy.orm.session import sessionmaker


def get_session(connection=None):
    session = sessionmaker(bind=engine)
    if connection:
        return session(bind=connection)
    return session()
