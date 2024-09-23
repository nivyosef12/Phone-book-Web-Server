import json

import app.api.contacts.utils as utils

from datetime import datetime
from app.api.contacts.models import Contact
from sqlalchemy.future import select
from sqlalchemy import and_
from app.common.utils import handle_exception
from app.common.logger import logger
from app.api.contacts.schemas import GetAllContacts

async def get_all_contancts(db_conn, input_data: GetAllContacts):
    limit = input_data.limit
    offset = input_data.offset
    logger.info(f"Getting contacts information for limit={limit}, offset={offset}")
    
    try:
        # TODO verify limit + offset dont excceed num of contacts?
        result_query = await db_conn.execute(
                select(Contact).where(Contact.deleted_ts.is_(None)).order_by(Contact.id).limit(limit).offset(offset)
            )
        
        contacts = result_query.scalars().all()
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
        logger.error(f"Error while getting contacts for limit={limit}, offset={offset} - {e}")
        return handle_exception(e)
