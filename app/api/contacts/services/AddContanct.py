import json

import app.api.contacts.utils as utils

from app.api.contacts.models import Contact
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.common.utils import handle_exception
from app.common.logger import logger



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
        new_contact = Contact(first_name=first_name, last_name=last_name,
                                phone_number=phone_number, address=address, deleted_ts=None)
        
        db_conn.add(new_contact)
        await db_conn.commit()
        
        logger.info(f"{first_name} added sucessfuly")
        return 200, json.dumps({"status": "ok"})
    
    except IntegrityError as e:
        if 'unique constraint' in str(e.orig):
            logger.error(f"Duplicate entry for phone number: {phone_number}")
        
        else:
            logger.error(f"IntegrityError occurred: {e.orig}")

        return handle_exception(e)

    except Exception as e:
        logger.error(f"Error while adding contact - {e}")
        return handle_exception(e)