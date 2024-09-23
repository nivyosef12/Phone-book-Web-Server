import httpx
import asyncio
import logging
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.main import app
from app.api.contacts.models import Contact
from app.common.db import get_db
from app.common.utils import get_env_variable
from tests.utils import random_phone_number, random_string
from datetime import datetime

class TestGetContact:

    @classmethod
    def setup_class(cls):
        cls.number_of_not_deleted_contacts = 15
        cls.number_of_deleted_contacts = 1
        async def inner():
            phone_numbers = set()
            async for db_conn in get_db():
                for i in range(cls.number_of_not_deleted_contacts):
                    # Generate unique phone number
                    phone_number = random_phone_number()
                    while phone_number in phone_numbers:
                        phone_number = random_phone_number()
                    phone_numbers.add(f"{i}{phone_number}")

                    new_contact = Contact(
                        first_name=random_string(), 
                        last_name=random_string(),
                        phone_number=phone_number, 
                        address=random_string()
                    )
                    db_conn.add(new_contact)
                
                # add one contact for deleted_ts test
                phone_number = random_phone_number()
                while phone_number in phone_numbers:
                    phone_number = random_phone_number()
                phone_numbers.add(f"{phone_number}")
                new_contact = Contact(
                        first_name=random_string(), 
                        last_name=random_string(),
                        phone_number=phone_number, 
                        address=random_string(),
                        deleted_ts=datetime.now()
                    )
                db_conn.add(new_contact)

                await db_conn.commit()
        asyncio.get_event_loop().run_until_complete(inner())
    
    @classmethod
    def teardown_class(cls):
        # delete all added contacts
        async def inner():
            try:
                async for db_conn in get_db():
                    stmt = delete(Contact)
                    result = await db_conn.execute(stmt)
                    await db_conn.commit()
                    
                    deleted_count = result.rowcount
                    if deleted_count != cls.number_of_not_deleted_contacts + cls.number_of_deleted_contacts:
                        raise Exception(f"deleted count({deleted_count}) != contacts_number({cls.number_of_not_deleted_contacts + + cls.number_of_deleted_contacts})")
            except Exception as e:
                logging.error(f"Error while deleting contacts - {e}")
                raise e
            
        asyncio.get_event_loop().run_until_complete(inner())

    def test_get_all_contacts(self):
        async def inner():
            # Setup client
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                fetched_contacts = set()
                limit = 4
                offset = 0

                while True:
                    # get curr page
                    logging.info(f"getting contacts - limit={limit}, offset={offset}")
                    response = await client.get(f"/api/contacts/get?limit={limit}&offset={offset}")
                    response_dict = response.json()
                    assert response.status_code == 200, f"Failed to get contacts - {response.json()}"

                    for key in response_dict:
                        assert response_dict[key]['phone_number'] not in fetched_contacts, f"{response_dict[key]} already featched"
                        fetched_contacts.add(response_dict[key]['phone_number'])

                    # stop cond
                    if len(response_dict) == 0:
                        assert len(fetched_contacts) > 0, f"0 contacts returned"
                        break

                    # assert last page contains self.number_of_not_deleted_contacts % limit contacts
                    assert len(response_dict) == limit or len(response_dict) == self.number_of_not_deleted_contacts % limit, f"fetched response does not contain the expected number of results. limit={limit}, offset={offset}, response_len={len(response_dict)}, last_page={self.number_of_not_deleted_contacts % limit}"

                    # update offset
                    offset += limit


                assert len(fetched_contacts) == self.number_of_not_deleted_contacts, f"not all contact returned. fetched_contacts({len(fetched_contacts)})={fetched_contacts}\n != {self.number_of_not_deleted_contacts}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_get_all_limit_at_max(self):
        async def inner():
            # Setup client
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                limit = int(get_env_variable("LIMIT_CONTACTS_RESPONSE"))
                offset = 0

                # get curr page
                logging.info(f"getting contacts - limit={limit}, offset={offset}")
                response = await client.get(f"/api/contacts/get?limit={limit}&offset={offset}")
                assert response.status_code == 200, f"Failed to get contacts - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_get_all_negative_limit(self):
        async def inner():
            # Setup client
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                limit = -1
                offset = 0

                # get curr page
                logging.info(f"getting contacts - limit={limit}, offset={offset}")
                response = await client.get(f"/api/contacts/get?limit={limit}&offset={offset}")
                assert response.status_code == 422, f"Failed to get contacts - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_get_all_more_then_max__limit(self):
        async def inner():
            # Setup client
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                limit = int(get_env_variable("LIMIT_CONTACTS_RESPONSE")) + 1
                offset = 0

                # get curr page
                logging.info(f"getting contacts - limit={limit}, offset={offset}")
                response = await client.get(f"/api/contacts/get?limit={limit}&offset={offset}")
                assert response.status_code == 422, f"Failed to get contacts - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_get_all_negative_offset(self):
        async def inner():
            # Setup client
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                # Add contact
                limit = 1
                offset = -1

                # get curr page
                logging.info(f"getting contacts - limit={limit}, offset={offset}")
                response = await client.get(f"/api/contacts/get?limit={limit}&offset={offset}")
                assert response.status_code == 422, f"Failed to get contacts - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())


    
