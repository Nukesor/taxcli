from taxcli.models import Contact
from taxcli.helper.postgres import get_session


def get_contact_data():
    session = get_session()

    alias = None
    name = None
    addressline1 = None
    addressline2 = None
    addressline3 = None
    city = None
    zip_or_postcode = None
    state_province_county = None
    country = None

    while not alias:
        alias = input('Enter an alias for this contact:')
        exists = session.query(Contact).get(alias)
        if exists or alias == 'help':
            print('Alias already exists')
            alias = None

    while not name:
        name = input('Enter the name of this contact:')

    print('Please enter the Address of this contact:')
    while not addressline1:
        addressline1 = input("First address line:")

    addressline2 = input('Additional address information:')
    if addressline2:
        addressline3 = input('Additional address information:')
    else:
        addressline2 = None

    while not city:
        city = input('city:')

    while not zip_or_postcode:
        zip_or_postcode = input('zip or postcode:')

    state_province_county = input("State province county:")
    state_province_county = None if state_province_county == '' else state_province_county

    while not country:
        country = input("country:")

    new_contact = Contact(alias, name, addressline1,
                          city, zip_or_postcode, country)

    new_contact.addressline2 = addressline2
    new_contact.addressline3 = addressline3
    new_contact.state_province_county = state_province_county

    session.add(new_contact)
    session.commit()
