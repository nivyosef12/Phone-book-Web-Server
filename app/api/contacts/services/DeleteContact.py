import json

import app.api.contacts.utils as utils
from datetime import datetime

from app.api.contacts.models import Contact
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.common.utils import handle_exception
from app.common.logger import logger

def validate_input(phone_number, first_name, last_name):
    if phone_number is not None and not utils.is_valid_phone_number(phone_number):
        log_msg = f"Error editing contact. Invalid phone number - {phone_number}"
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

async def delete_contact(db_conn, phone_number=None, first_name=None, last_name=None):
    try:
        # check if input is valid
        validate_input(phone_number, first_name, last_name)
        
        # build dynamic query
        query = select(Contact).where(Contact.deleted_ts.is_(None))

        if phone_number:
            query = query.where(Contact.phone_number == phone_number)
        if first_name:
            query = query.where(Contact.first_name == first_name)
        if last_name:
            query = query.where(Contact.last_name == last_name)

        logger.debug(f"\n\n\n{query}\n\n\n")

        # execute query
        result = await db_conn.execute(query)
        contacts = result.scalars().all()

        # check if contact exists
        if contacts is None or len(contacts) == 0:
            logger.error("No contacts found matching the criteria")
            return handle_exception(ValueError("No contacts found matching the criteria"))

        # mark contacts as deleted
        for contact in contacts:
            contact.deleted_ts = datetime.now()

        await db_conn.commit()

        logger.info(f"Deleted {len(contacts)} contact(s)")
        return 200, json.dumps({"status": "ok", "message": f"Deleted {len(contacts)} contact(s)"})
    
    except IntegrityError as e:
        if 'unique constraint' in str(e.orig):
            logger.error(f"Duplicate entry for phone number: {phone_number}")
            return handle_exception(ValueError("Duplicate entry for phone number."))
        
        logger.error(f"IntegrityError occurred: {e.orig}")
        return handle_exception(e)

    except Exception as e:
        logger.error(f"Error while updating contact - {e}")
        return handle_exception(e)