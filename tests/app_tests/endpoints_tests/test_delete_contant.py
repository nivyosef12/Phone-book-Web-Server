import httpx
import asyncio
import logging
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select
from app.main import app
from app.api.contacts.models import Contact
from app.common.db import get_db
from datetime import datetime

class TestDelteContact:

    @classmethod
    def setup_class(cls):
        cls.contacts = [
            {"phone_number": "1111111111", "first_name": "aaa", "last_name": "bbb", "address": "TLV", "deleted_ts": None},
            {"phone_number": "2222222222", "first_name": "aaron", "last_name": "ccc", "address": "Jerusalem", "deleted_ts": None},
            {"phone_number": "3333333333", "first_name": "ann", "last_name": "ddd", "address": "Haifa", "deleted_ts": None},
            {"phone_number": "4444444444", "first_name": "ann", "last_name": "ddd", "address": "Haifa", "deleted_ts": None},
            {"phone_number": "5555555555", "first_name": "asnn", "last_name": "dfdd", "address": "Haifa", "deleted_ts": None},
            {"phone_number": "6666666666", "first_name": "ann", "last_name": "ddd", "address": "Haifa", "deleted_ts": None},
            {"phone_number": "7777777777", "first_name": "ann", "last_name": "ddd", "address": "Haifa", "deleted_ts": None},
            {"phone_number": "8888888888", "first_name": "bob", "last_name": "smith", "address": "Beer Sheva", "deleted_ts": datetime.now()}
        ]
        async def inner():
            async for db_conn in get_db():
                for contact in cls.contacts:
                    new_contact = Contact(
                        first_name=contact['first_name'], 
                        last_name=contact['last_name'],
                        first_name_lower=contact['first_name'].lower(), 
                        last_name_lower=contact['last_name'].lower(),
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
    
    def test_delete_contact_no_arguments(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"searching contacts with no arguments")
                response = await client.post(f"/api/contacts/delete", json={})
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_by_phone_success(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_delete = self.contacts[0]
                response = await client.post(f"/api/contacts/delete", json={
                    "phone_number": contact_to_delete["phone_number"]
                })

                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                
                # assert add endpoint worked
                logging.info(f"Getting info from db where phone number = {contact_to_delete['phone_number']}")
                async for db_conn in get_db():
                    deleted_contact = await self.get_contact_from_db(contact_to_delete["phone_number"], db_conn)

                assert deleted_contact.deleted_ts is not None, f"deleted_ts is None {deleted_contact.phone_number}, {deleted_contact.deleted_ts}"

        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_delete_contact_by_first_name(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_delete = self.contacts[1]
                response = await client.post(f"/api/contacts/delete", json={
                    "first_name": contact_to_delete["first_name"]
                })

                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                
                # assert add endpoint worked
                logging.info(f"Getting info from db where phone number = {contact_to_delete['phone_number']}")
                async for db_conn in get_db():
                    deleted_contact = await self.get_contact_from_db(contact_to_delete["phone_number"], db_conn)

                assert deleted_contact.deleted_ts is not None, f"deleted_ts is None {deleted_contact.phone_number}, {deleted_contact.deleted_ts}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_by_last_name(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_delete = self.contacts[2]
                contact_to_delete_2 = self.contacts[3]
                response = await client.post(f"/api/contacts/delete", json={
                    "last_name": contact_to_delete["last_name"]
                })

                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                
                # assert add endpoint worked
                logging.info(f"Getting info from db where phone number = {contact_to_delete['phone_number']}")
                async for db_conn in get_db():
                    deleted_contact = await self.get_contact_from_db(contact_to_delete["phone_number"], db_conn)
                    deleted_contact_2 = await self.get_contact_from_db(contact_to_delete_2["phone_number"], db_conn)

                assert deleted_contact.deleted_ts is not None, f"deleted_ts is None {deleted_contact.phone_number}, {deleted_contact.deleted_ts}"
                assert deleted_contact_2.deleted_ts is not None, f"deleted_ts is None {deleted_contact_2.phone_number}, {deleted_contact_2.deleted_ts}"

        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_delete_contact_by_all_fields_success(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                contact_to_delete = self.contacts[4]

                response = await client.post(f"/api/contacts/delete", json={
                    "phone_number": contact_to_delete["phone_number"],
                    "first_name": contact_to_delete["first_name"],
                    "last_name": contact_to_delete["last_name"]

                })

                assert response.status_code == 200, f"Status code not correct {response.status_code} - {response.json()}"
                
                # assert add endpoint worked
                logging.info(f"Getting info from db where phone number = {contact_to_delete['phone_number']}")
                async for db_conn in get_db():
                    deleted_contact = await self.get_contact_from_db(contact_to_delete["phone_number"], db_conn)

                assert deleted_contact.deleted_ts is not None, f"deleted_ts is None {deleted_contact.phone_number}, {deleted_contact.deleted_ts}"

        asyncio.get_event_loop().run_until_complete(inner())
    
  
    def test_delete_contact_phone_not_found(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={
                    "phone_number": "9999999999"  # Phone number not in contacts
                })

                assert response.status_code == 404, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_first_name_not_found(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={
                    "first_name": "nonexistent"
                })

                assert response.status_code == 404, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_last_name_not_found(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={
                    "last_name": "nonexistent"
                })

                assert response.status_code == 404, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_delete_contact_invalid_phone(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={
                    "phone_number": "not_a_phone"
                })
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_empty_first_name(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={
                    "first_name": ""
                })
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_invalid_last_name(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={
                    "last_name": "12345"
                })
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_no_fields_provided(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={})
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_with_nonexistent_phone(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={
                    "phone_number": "0000000000"  # Assuming this number doesn't exist
                })
                assert response.status_code == 404, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_delete_contact_invalid_fields_combination(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(f"/api/contacts/delete", json={
                    "phone_number": "invalid_phone",
                    "first_name": "aaa",
                    "last_name": "bbb"
                })
                assert response.status_code == 422, f"Status code not correct {response.status_code} - {response.json()}"

        asyncio.get_event_loop().run_until_complete(inner())

