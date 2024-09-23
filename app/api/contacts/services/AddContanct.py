import json

import app.api.contacts.utils as utils
from datetime import datetime

from app.api.contacts.models import Contact
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.common.utils import handle_exception
from app.common.logger import logger
from app.common.exceptions import ConflictError
from app.api.contacts.schemas import AddContactInput

async def add_contact(db_conn, add_contact_input: AddContactInput):
    first_name = add_contact_input.first_name
    last_name = add_contact_input.last_name
    phone_number = add_contact_input.phone_number
    address = add_contact_input.address
    
    try:
        # fetch the existing contact by phone number
        result = await db_conn.execute(
                select(Contact).where(Contact.phone_number == phone_number)
            )
        contact = result.scalar_one_or_none()

        # no such contact ever existed
        if contact is None:
            new_contact = Contact(first_name=first_name, last_name=last_name,
                                    phone_number=phone_number, address=address, deleted_ts=None)
            
            db_conn.add(new_contact)
            await db_conn.commit()
            response = f"{first_name} added successfully."
            logger.info(response)
        
        # contact used to exist but was deleted
        elif contact.deleted_ts is not None:
            contact.phone_number = phone_number
            contact.first_name = first_name
            contact.last_name = last_name
            contact.address = address
            contact.updated_ts = datetime.now() 
            contact.deleted_ts = None

            await db_conn.commit()
            response = f"{first_name} added successfully."
            logger.info(response)

        # contact exists and is not deleted
        else:
            raise ConflictError(f"phone number = {phone_number} already exists")

        return 201, json.dumps({"status": "ok", "message": response})
    
    except ConflictError as e:
        logger.error(f"IntegrityError on add_contact endpoint - {e}")
        return handle_exception(e)

    except Exception as e:
        logger.error(f"Error while adding contact - {e}")
        return handle_exception(e)