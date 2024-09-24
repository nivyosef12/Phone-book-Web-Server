import httpx
import asyncio
import logging
import json
import random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select
from app.main import app
from app.api.contacts.models import Contact
from app.common.db import get_db
from datetime import datetime

class TestEditContact:

    @classmethod
    def setup_class(cls):
        cls.contacts = [
            {"phone_number": "1111111111", "first_name": "aaa", "last_name": "bbb", "address": "TLV", "deleted_ts": None},
            {"phone_number": "2222222222", "first_name": "aaron", "last_name": "ccc", "address": "Jerusalem", "deleted_ts": None},
            {"phone_number": "3333333333", "first_name": "ann", "last_name": "ddd", "address": "Haifa", "deleted_ts": None},
            {"phone_number": "4444444444", "first_name": "bob", "last_name": "smith", "address": "Beer Sheva", "deleted_ts": None},
            {"phone_number": "5555555555", "first_name": "bob", "last_name": "smith", "address": "Beer Sheva", "deleted_ts": None},
            {"phone_number": "6666666666", "first_name": "slim", "last_name": "shady", "address": "Detroit", "deleted_ts": None},
            {"phone_number": "7777777777", "first_name": "slim", "last_name": "shady", "address": "Detroit", "deleted_ts": datetime.now()},
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
        pass
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

    async def get_contact_from_db(self, phone_number, db_conn: AsyncSession):
        result = await db_conn.execute(
            select(Contact).where(Contact.phone_number == phone_number)
        )
        return result.scalars().first()
    
    def test_edit_contact_no_arguments(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts with no arguments")

                contact_to_edit = self.contacts[0]
                response = await client.post(f"/api/contacts/edit", json={"phone_number": contact_to_edit["phone_number"]})
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_edit_contact_with_valid_data(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_edit = self.contacts[1]

                new_phone_number = "+12345678901"
                new_first_name = "Updated"
                new_last_name = "Name"
                new_address = "new"
                response = await client.post(f"/api/contacts/edit", json={
                    "phone_number": contact_to_edit["phone_number"],
                    "new_phone_number": new_phone_number,
                    "first_name": new_first_name,
                    "last_name": new_last_name,
                    "address": new_address
                })

                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                
                # assert add endpoint worked
                logging.info(f"Getting info from db where phone number = {contact_to_edit['phone_number']}")
                async for db_conn in get_db():
                    prev_new_edited_contact = await self.get_contact_from_db(contact_to_edit["phone_number"], db_conn)
                    new_edited_contact = await self.get_contact_from_db(new_phone_number, db_conn)

                assert prev_new_edited_contact is None, f"Contact with phone number = {contact_to_edit['phone_number']} should not exist in the database."
                assert new_edited_contact is not None, f"Contact {new_first_name} should exist in the database."
                assert new_edited_contact.first_name == new_first_name, f"First name is note the same -> {new_edited_contact.first_name} != {new_first_name}"
                assert new_edited_contact.last_name == new_last_name, f"Last name is note the same -> {new_edited_contact.last_name} != {new_last_name}"
                assert new_edited_contact.phone_number == new_phone_number, f"Phone number is note the same -> {new_edited_contact.phone_number} != {new_phone_number}"
                assert new_edited_contact.address == new_address, f"Address is note the same -> {new_edited_contact.address} != {new_address}"
                assert new_edited_contact.created_ts is not None, f"created_ts is None"
                assert new_edited_contact.updated_ts is not None, f"updated_ts is None"
                assert new_edited_contact.deleted_ts is None, f"deleted_ts is not None"

        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_edit_non_existing_contact(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/edit", json={
                    "phone_number": "65555555555",
                    "new_phone_number": "+12345678901"
                })

                assert response.status_code == 404, f"Status code not correct {response.status_code} - {response.json()}"
        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_edit_contact_invalid_phone_number(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_edit = self.contacts[2]

                response = await client.post(f"/api/contacts/edit", json={
                    "phone_number": contact_to_edit["phone_number"],
                    "new_phone_number": "invalid_phone_format"
                })

                assert response.status_code == 422, f"Expected status code 422 for invalid phone number - {response.json()}"
        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_edit_contact_duplicate_phone_number(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_edit = self.contacts[3]
                existing_contact = self.contacts[4]

                response = await client.post(f"/api/contacts/edit", json={
                    "phone_number": contact_to_edit["phone_number"],
                    "new_phone_number": existing_contact["phone_number"],  # set a duplicate phone number
                })

                assert response.status_code == 409, f"Expected status code 409 for duplicate phone number - {response.json()}"
        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_edit_contact_non_nullable_fields(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_edit = self.contacts[5]

                response = await client.post(f"/api/contacts/edit", json={
                    "phone_number": contact_to_edit["phone_number"],
                    "new_phone_number": None,  # Invalid since it's required
                })

                assert response.status_code == 422, f"Expected status code 422 for non-nullable field - {response.json()}"
        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_edit_deleted_contact(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_edit = self.contacts[6]

                response = await client.post(f"/api/contacts/edit", json={
                    "phone_number": contact_to_edit["phone_number"],
                    "new_phone_number": "4444",  # Invalid since it's required
                })

                assert response.status_code == 404, f"Expected status code 404 for deleted contact edit - {response.json()}"
        asyncio.get_event_loop().run_until_complete(inner())







   