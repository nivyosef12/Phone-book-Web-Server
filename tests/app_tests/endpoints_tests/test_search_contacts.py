import httpx
import asyncio
import logging
import json
import random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.main import app
from app.api.contacts.models import Contact
from app.common.db import get_db
from datetime import datetime
class TestSearchContact:

    @classmethod
    def setup_class(cls):
        cls.contacts = [
            {"phone_number": "1111111111", "first_name": "aaa", "last_name": "bbb", "address": "TLV", "deleted_ts": None},
            {"phone_number": "2222222222", "first_name": "aaron", "last_name": "ccc", "address": "Jerusalem", "deleted_ts": None},
            {"phone_number": "3333333333", "first_name": "ann", "last_name": "ddd", "address": "Haifa", "deleted_ts": None},
            {"phone_number": "4444444444", "first_name": "bob", "last_name": "smith", "address": "Beer Sheva", "deleted_ts": None},
            {"phone_number": "5555555555", "first_name": "slim", "last_name": "shady", "address": "Detroit", "deleted_ts": datetime.now()},
        ]
        async def inner():
            async for db_conn in get_db():
                for contact in cls.contacts:
                    new_contact = Contact(
                        first_name=contact['first_name'], 
                        last_name=contact['last_name'],
                        phone_number=contact['phone_number'], 
                        address=contact['address'],
                        deleted_ts=contact['deleted_ts']
                    )
                    db_conn.add(new_contact)
                
                await db_conn.commit()
        asyncio.get_event_loop().run_until_complete(inner())
    
    @classmethod
    def teardown_class(cls):
        async def inner():
            try:
                async for db_conn in get_db():
                    stmt = delete(Contact)
                    result = await db_conn.execute(stmt)
                    await db_conn.commit()

                    deleted_count = result.rowcount
                    if deleted_count != len(cls.contacts):
                        raise Exception(f"deleted count({deleted_count}) != contacts_number({len(cls.contacts)})")
            except Exception as e:
                logging.error(f"Error while deleting contacts - {e}")
                raise e
            
        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_no_criteria(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts with no criteria")
                response = await client.get(f"/api/contacts/search")
                assert response.status_code == 400, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_by_phone_number(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_search = random.choice(self.contacts)
                while contact_to_search['deleted_ts'] is not None:
                    contact_to_search = random.choice(self.contacts)

                logging.info(f"searching contacts by phone number=({contact_to_search['phone_number']}) prefix")
                response = await client.get(f"/api/contacts/search?phone_number={contact_to_search['phone_number'][0:3]}")
                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                contacts = response.json()
                assert len(contacts) == 1, f"Expected 1 contact, got {len(contacts)}"

                contact_info = list(contacts.values())[0]
                assert contact_info["first_name"] == contact_to_search['first_name'], f"Expected {contact_to_search['first_name']}, got {contact_info['first_name']}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_by_first_name(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts by first name prefix")
                response = await client.get(f"/api/contacts/search?first_name=aa")
                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                contacts = response.json()
                assert len(contacts) == 2, f"Expected 2 contacts, got {len(contacts)}"
                first_names = [contact['first_name'] for contact in contacts.values()]
                assert "aaa" in first_names and "aaron" in first_names, f"Expected 'aaa' and 'aaron', got {first_names}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_by_last_name(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_search = random.choice(self.contacts)
                while contact_to_search['deleted_ts'] is not None:
                    contact_to_search = random.choice(self.contacts)

                logging.info(f"searching contacts by last_name=({contact_to_search['last_name']}) prefix")
                response = await client.get(f"/api/contacts/search?last_name={contact_to_search['last_name'][0:2]}")
                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                contacts = response.json()
                assert len(contacts) == 1, f"Expected 1 contact, got {len(contacts)}"

                contact_info = list(contacts.values())[0]
                assert contact_info['last_name'] == contact_to_search['last_name'], f"Expected {contact_to_search['last_name']}, got {contact_info['last_name']}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_combined_criteria(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts by first name and phone number prefix")
                response = await client.get(f"/api/contacts/search?first_name=a&phone_number=222")
                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                contacts = response.json()
                assert len(contacts) == 1, f"Expected 1 contact, got {len(contacts)}"

                contact_info = list(contacts.values())[0]
                assert contact_info['first_name'] == "aaron", f"Expected 'aaron', got {contact_info['first_name']}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_no_results(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts with no match")
                response = await client.get(f"/api/contacts/search?phone_number=999")
                assert response.status_code == 404, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_search_deleted_contact(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts with no match")
                response = await client.get(f"/api/contacts/search?phone_number=555")
                assert response.status_code == 404, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_bad_input(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(f"/api/contacts/search?first_name=a1b")
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"
                
                response = await client.get(f"/api/contacts/search?last_name=a1b")
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"
                
                response = await client.get(f"/api/contacts/search?phone_number=a3a")
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"
                
        asyncio.get_event_loop().run_until_complete(inner())