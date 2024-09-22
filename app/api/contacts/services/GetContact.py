import json

import app.api.contacts.utils as utils

from datetime import datetime
from app.api.contacts.models import Contact
from sqlalchemy.future import select
from app.common.utils import handle_exception
from app.common.logger import logger


async def get_contanct(db_conn, phone_number: str):
    logger.info(f"Getting contact information for phune_number={phone_number}")

    if not utils.is_valid_phone_number(phone_number):
        log_msg = f"Error getting contact by phone number. Invalid phone number - {phone_number}"
        logger.error(log_msg)
        return handle_exception(ValueError(log_msg))
    try:
        result = await db_conn.execute(
                select(Contact).where(Contact.phone_number == phone_number)
            )
        contact = result.scalar_one_or_none()

        if not contact:
            log_msg = f"Error getting contact by phone number. Contact inforamtion not found"
            logger.error(log_msg)
            return handle_exception(ValueError(log_msg))
        
        logger.info(contact)
        res = {
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "phone_number": contact.phone_number,
                "address": contact.address,
                "created_ts": str(contact.created_ts),
                "updated_ts": str(contact.updated_ts),
                "deleted_ts": str(contact.deleted_ts),
            }
         
        return 200, json.dumps(res)
    
    except Exception as e:
        logger.error(f"Error while getting contact by phone - {e}")
        return handle_exception(e)