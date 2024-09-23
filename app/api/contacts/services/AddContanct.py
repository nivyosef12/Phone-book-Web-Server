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



def is_valid_input(first_name, last_name, phone_number):
    if not utils.is_valid_phone_number(phone_number):
        log_msg = f"Error adding contact Invalid phone number - {phone_number}"
        return False, log_msg
    
    if not utils.is_valid_name(first_name, last_name):
        log_msg = f"Error adding contact. Invalid name - {first_name} {last_name if last_name is not None else ''}"
        logger.error(log_msg)
        return False, log_msg
    
    return True, "ok"

async def add_contact(db_conn, first_name, phone_number, last_name=None, address=None):

    # check if input is valid
    is_valid, msg = is_valid_input(first_name, last_name, phone_number)
    if not is_valid:
        logger.error(msg)
        return handle_exception(ValueError(msg))
    
    try:
        # fetch the existing contact by phone number
        result = await db_conn.execute(
                select(Contact).where(and_(
                    Contact.phone_number == phone_number,
                    Contact.deleted_ts.is_(None)
                ))
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

        return 200, json.dumps({"status": "ok", "message": response})
    
    except ConflictError as e:
        logger.error(f"IntegrityError on add_contact endpoint - {e}")
        return handle_exception(e)

    except Exception as e:
        logger.error(f"Error while adding contact - {e}")
        return handle_exception(e)