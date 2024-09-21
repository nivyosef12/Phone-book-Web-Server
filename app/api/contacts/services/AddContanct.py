import logging
import json

from app.api.contacts.models import Contact


async def add_contact(db_conn, first_name, phone_number, last_name=None, address=None):
    # TODO check input valid and if this phone number in use

    new_contact = Contact(first_name=first_name, last_name=last_name,
                              phone_number=phone_number, address=address)
    
    db_conn.add(new_contact)
    await db_conn.commit()
    
    return 200, json.dumps({"status": "ok"})