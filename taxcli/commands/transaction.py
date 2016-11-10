from taxcli.helper.postgres import get_session

def get_transaction_data(args):
    session = get_session()
