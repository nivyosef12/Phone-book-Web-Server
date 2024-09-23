import httpx
import asyncio
import logging
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.main import app
from app.api.contacts.models import Contact
from app.common.db import get_db
from tests.utils import random_phone_number, random_string

class TestSearchContact:

    @classmethod
    def setup_class(cls):
        cls.contacts = [
            {"phone_number": "1111111111", "first_name": "aaa", "last_name": "bbb", "address": "TLV"},
            {"phone_number": "2222222222", "first_name": "aaron", "last_name": "ccc", "address": "Jerusalem"},
            {"phone_number": "3333333333", "first_name": "ann", "last_name": "ddd", "address": "Haifa"},
            {"phone_number": "4444444444", "first_name": "bob", "last_name": "smith", "address": "Beer Sheva"},
        ]
        async def inner():
            async for db_conn in get_db():
                for contact in cls.contacts:
                    new_contact = Contact(
                        first_name=contact['first_name'], 
                        last_name=contact['last_name'],
                        phone_number=contact['phone_number'], 
                        address=contact['address']
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
                logging.info(f"searching contacts by phone number prefix")
                response = await client.get(f"/api/contacts/search?phone_number=111")
                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                contacts = response.json()
                assert len(contacts) == 1, f"Expected 1 contact, got {len(contacts)}"
                assert contacts['1']['first_name'] == "aaa", f"Expected 'aaa', got {contacts['1']['first_name']}"

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
                logging.info(f"searching contacts by last name prefix")
                response = await client.get(f"/api/contacts/search?last_name=sm")
                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                contacts = response.json()
                assert len(contacts) == 1, f"Expected 1 contact, got {len(contacts)}"
                assert contacts['4']['last_name'] == "smith", f"Expected 'smith', got {contacts['4']['last_name']}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_combined_criteria(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts by first name and phone number prefix")
                response = await client.get(f"/api/contacts/search?first_name=a&phone_number=222")
                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                contacts = response.json()
                assert len(contacts) == 1, f"Expected 1 contact, got {len(contacts)}"
                assert contacts['2']['first_name'] == "aaron", f"Expected 'aaron', got {contacts['2']['first_name']}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_search_contact_no_results(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts with no match")
                response = await client.get(f"/api/contacts/search?phone_number=999")
                assert response.status_code == 404, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())
