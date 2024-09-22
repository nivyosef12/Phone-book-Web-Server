import json

import app.api.contacts.utils as utils
from datetime import datetime

from app.api.contacts.models import Contact
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.common.utils import handle_exception
from app.common.logger import logger

def validate_input(new_phone_number, first_name, last_name):
    if new_phone_number is not None and not utils.is_valid_phone_number(new_phone_number):
        log_msg = f"Error editing contact. Invalid phone number - {new_phone_number}"
        logger.error(log_msg)
        raise ValueError(log_msg)
    
    if first_name is not None and not utils.is_valid_name(first_name):
        log_msg = f"Error editing contact. Invalid first name - {first_name}"
        logger.error(log_msg)
        raise ValueError(log_msg)

    if last_name is not None and not utils.is_valid_name(last_name):
        log_msg = f"Error editing contact. Invalid last name - {last_name}"
        logger.error(log_msg)
        raise ValueError(log_msg)

async def edit_contact(db_conn, phone_number, new_phone_number=None, first_name=None, last_name=None, address=None):
    try:
        # check if input is valid
        validate_input(new_phone_number, first_name, last_name)
        
        # fetch the existing contact by phone number
        result = await db_conn.execute(
            select(Contact).where(Contact.phone_number == phone_number and Contact.deleted_ts.is_(None))
        )
        contact = result.scalar_one_or_none()

        # check if contact exists
        if contact is None:
            log_msg = f"Contact with phone number {phone_number} not found."
            logger.error(log_msg)
            return handle_exception(ValueError(log_msg))

        # update relevant contact fields (new_phone_number and first_name are not allowed to be None)
        if new_phone_number is not None:
            contact.phone_number = new_phone_number
        if first_name is not None:
            contact.first_name = first_name
        
        contact.last_name = last_name
        contact.address = address
        contact.updated_ts = datetime.now() 

        await db_conn.commit()

        logger.info(f"Contact with phone number {phone_number if new_phone_number is None else new_phone_number} updated successfully.")
        return 200, json.dumps({"status": "ok", "message": "Contact updated successfully."})

    except IntegrityError as e:
        if 'unique constraint' in str(e.orig):
            logger.error(f"Duplicate entry for phone number: {phone_number}")
            return handle_exception(ValueError("Duplicate entry for phone number."))
        
        logger.error(f"IntegrityError occurred: {e.orig}")
        return handle_exception(e)

    except Exception as e:
        logger.error(f"Error while updating contact - {e}")
        return handle_exception(e)