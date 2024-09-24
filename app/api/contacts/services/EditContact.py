import json

import app.api.contacts.utils as utils
from datetime import datetime

from app.api.contacts.models import Contact
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from app.common.utils import handle_exception
from app.common.logger import logger
from app.api.contacts.schemas import EditContactInput
from app.common.exceptions import ConflictError

async def edit_contact(db_conn, edit_contact_input: EditContactInput):
    phone_number = edit_contact_input.phone_number
    new_phone_number = edit_contact_input.new_phone_number
    first_name = edit_contact_input.first_name
    last_name = edit_contact_input.last_name
    address = edit_contact_input.address
    try:
        
        # fetch the existing contact by phone number
        result = await db_conn.execute(
                select(Contact).where(and_(
                    Contact.phone_number == phone_number,
                    Contact.deleted_ts.is_(None)
                ))
            )
        contact = result.scalar_one_or_none()

        # check if contact exists
        if contact is None:
            log_msg = f"Contact with phone number {phone_number} not found."
            logger.error(log_msg)
            return handle_exception(ValueError(log_msg))

        # update relevant contact fields (new_phone_number and first_name are not allowed to be None)
        if new_phone_number is not None:

            # verify new_phone number not in DB
            new_phone_result = await db_conn.execute(
                    select(Contact).where(and_(
                        Contact.phone_number == new_phone_number,
                        Contact.deleted_ts.is_(None)
                    ))
                )
            existing_contact = new_phone_result.scalar_one_or_none()
            if existing_contact is not None:
                log_msg = f"Contact with phone number {phone_number} already exists."
                logger.error(log_msg)
                return handle_exception(ConflictError(log_msg))
            
            contact.phone_number = new_phone_number
        if first_name is not None:
            contact.first_name_lower = first_name.lower()
            contact.first_name = first_name
        
        contact.last_name = last_name
        contact.last_name_lower = last_name.lower() if last_name is not None else None
        contact.address = address
        contact.updated_ts = datetime.now() 
        contact.deleted_ts = None

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