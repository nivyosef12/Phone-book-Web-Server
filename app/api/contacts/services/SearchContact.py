import json

import app.api.contacts.utils as utils
from datetime import datetime

from app.api.contacts.models import Contact
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.common.utils import handle_exception
from app.common.logger import logger
from app.common.exceptions import RecordNotFound


# TODO remove that
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

async def search_contact(db_conn, phone_number=None, first_name=None, last_name=None):
    
    try:
         # check if input is valid
        validate_input(phone_number, first_name, last_name)

        # build dynamic query
        query = select(Contact).where(Contact.deleted_ts.is_(None))
        if phone_number:
            query = query.where(Contact.phone_number.ilike(f'{phone_number}%'))
        if first_name:
            query = query.where(Contact.first_name.ilike(f'{first_name}%'))       
        if last_name:
            query = query.where(Contact.last_name.ilike(f'{last_name}%'))

        logger.debug(f"\n\n\n{query}\n\n\n")
        # execute query and fetch all matching contacts
        result = await db_conn.execute(query)
        contacts = result.scalars().all()

         # check if contact exists
        if contacts is None or len(contacts) == 0:
            logger.error("No contacts found matching the criteria")
            return handle_exception(RecordNotFound("No contacts found matching the criteria"))
        
        logger.info(f"Fetched {len(contacts)} results")
        response = {}
        for contact in contacts:
            response[contact.id] = {
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "phone_number": contact.phone_number,
                "address": contact.address,
            }

        logger.info(f"Fetched {response} contacts")
        return 200, json.dumps(response)
    
    except Exception as e:
        logger.error(f"Error while searching contacts for phone_number={phone_number}, first_name={first_name}, last_name={last_name} - {e}")
        return handle_exception(e)
