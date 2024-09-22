import httpx
import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.main import app
from app.api.contacts.models import Contact
from app.common.db import get_db

class TestAddContact:

    @classmethod
    def setup_class(cls):
        cls.luffy = {
            "first_name": "Luffy",
            "phone_number": "+1234567890",
            "address": "East Blue"
        }
        cls.zoro = {
            "first_name": "Zoro",
            "last_name": "Roronua",
            "phone_number": "+1234567891",
            "address": "East Blue"
        }
        cls.zoro_other_phone = {
            "first_name": "Zoro",
            "last_name": "Roronua",
            "phone_number": "+12345677777",
            "address": "East Blue"
        }
        cls.sunji = {
            "first_name": "Sunji",
            "phone_number": "invalid_phone",
            "address": "East Blue"
        }
        cls.ussop = {
            "first_name": "Ussop",
            "phone_number": "+1234567893"
        }
        cls.numi = {
            "first_name": "Numi",
            "phone_number": "+1234566666",
            "address": "East Blue"
        }

    async def get_contact_from_db(self, phone_number, db_conn: AsyncSession):
        result = await db_conn.execute(
            select(Contact).where(Contact.phone_number == phone_number)
        )
        return result.scalars().first()

    def test_add_contact_success(self):

        async def inner():
            # setup client
            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                
                # add contact
                logging.info(f"Adding {self.zoro} as contact")
                response = await client.post("/api/contacts/add", json=self.zoro)
                assert response.status_code == 200, f"Failed to add user - {response.json()}"
                assert response.json() == {"status": "ok"}

                # assert add endpoint worked
                logging.info(f"Getting info from db where phone number = {self.zoro['phone_number']}")
                async for db_conn in get_db():
                    zoro_contact = await self.get_contact_from_db(self.zoro['phone_number'], db_conn)

                assert zoro_contact is not None, f"Contact {self.zoro['first_name']} should exist in the database."
                assert zoro_contact.first_name == self.zoro['first_name'], f"First name is note the same -> {zoro_contact.first_name} != {self.zoro['first_name']}"
                assert zoro_contact.last_name == self.zoro['last_name'], f"Last name is note the same -> {zoro_contact.last_name} != {self.zoro['last_name']}"
                assert zoro_contact.phone_number == self.zoro['phone_number'], f"Phone number is note the same -> {zoro_contact.phone_number} != {self.zoro['phone_number']}"
                assert zoro_contact.address == self.zoro['address'], f"Address is note the same -> {zoro_contact.address} != {self.zoro['address']}"
                assert zoro_contact.created_ts is not None, f"created_ts is None"
                assert zoro_contact.updated_ts is not None, f"updated_ts is None"
                assert zoro_contact.deleted_ts is None, f"deleted_ts is not None"

        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_missing_last_name(self):

        async def inner():
            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                
                # add contact
                logging.info(f"Adding {self.luffy} as contact")
                response = await client.post("/api/contacts/add", json=self.luffy)
                assert response.status_code == 200, f"Failed to add user - {response.json()}"
                assert response.json() == {"status": "ok"}

                logging.info(f"Getting info from db where phone number = {self.luffy['phone_number']}")
                async for db_conn in get_db():
                    luffy_contact = await self.get_contact_from_db(self.luffy['phone_number'], db_conn)

                # Assert contact in db
                assert luffy_contact is not None, f"Contact {self.luffy['first_name']} should exist in the database."
                assert luffy_contact.first_name == self.luffy['first_name'], f"First name is note the same -> {luffy_contact.first_name} != {self.luffy['first_name']}"
                assert luffy_contact.last_name is None, f"Last name is note the same -> {luffy_contact.last_name} is not None"
                assert luffy_contact.phone_number == self.luffy['phone_number'], f"Phone number is note the same -> {luffy_contact.phone_number} != {self.luffy['phone_number']}"
                assert luffy_contact.address == self.luffy['address'], f"Address is note the same -> {luffy_contact.address} != {self.luffy['address']}"
                assert luffy_contact.created_ts is not None, f"created_ts is None"
                assert luffy_contact.updated_ts is not None, f"updated_ts is None"
                assert luffy_contact.deleted_ts is None, f"deleted_ts is not None"
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_missing_first_name(self):
        async def inner():

            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/contacts/add", json={
                    "phone_number": "+1234567892",
                    "address": "East Blue"
                })
                assert response.status_code == 422, f"Expected 422 for missing first name - {response.json()}"
        asyncio.get_event_loop().run_until_complete(inner())
    
    def test_add_contact_missing_phone_number(self):
        async def inner():

            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/contacts/add", json={
                    "first_name": "some",
                    "last_name": "name",
                    "address": "East Blue"
                })
                assert response.status_code == 422, f"Expected 422 for missing phone number - {response.json()}"
        asyncio.get_event_loop().run_until_complete(inner())
        
    def test_add_contact_without_address(self):
        async def inner():

            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:

                logging.info(f"Adding {self.ussop} as contact")
                response = await client.post("/api/contacts/add", json=self.ussop)
                assert response.status_code == 200, f"Failed to add user without address - {response.json()}"
                assert response.json() == {"status": "ok"}

                # assert the contact was added without an address
                logging.info(f"Getting info from db where phone number = {self.ussop['phone_number']}")
                async for db_conn in get_db():
                    usopp_contact = await self.get_contact_from_db(self.ussop['phone_number'], db_conn)
                
                assert usopp_contact is not None, f"Contact {self.ussop['first_name']} should exist in the database."
                assert usopp_contact.first_name == self.ussop['first_name'], f"First name is note the same -> {usopp_contact.first_name} != {self.ussop['first_name']}"
                assert usopp_contact.last_name is None, f"Last name is note the same -> {usopp_contact.last_name} is not None"
                assert usopp_contact.phone_number == self.ussop['phone_number'], f"Phone number is note the same -> {usopp_contact.phone_number} != {self.ussop['phone_number']}"
                assert usopp_contact.address is None, f"Address is note the same -> {usopp_contact.address} is not None"
                assert usopp_contact.created_ts is not None, f"created_ts is None"
                assert usopp_contact.updated_ts is not None, f"updated_ts is None"
                assert usopp_contact.deleted_ts is None, f"deleted_ts is not None"
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_invalid_phone_number(self):
        async def inner():

            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/contacts/add", json=self.sunji)

                logging.info("Assert request failed")
                assert response.status_code == 404, f"Expected 400 for invalid phone number - {response.json()}"
                assert "Invalid phone number" in response.json()["error_msg"], "Error message should indicate invalid phone number."
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_duplicate_phone_number(self):
        async def inner():

            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                logging.info(f"Adding {self.numi} for the first time")
                await client.post("/api/contacts/add", json=self.numi)

                logging.info(f"Adding {self.numi} for the second time")
                response = await client.post("/api/contacts/add", json=self.numi)

                logging.info("Assert request failed")
                assert response.status_code == 400, f"Expected 400 for duplicate phone number - {response.json()}"
                assert "Integrity Error" in response.json()["error_msg"], "Error message should indicate duplicate entry."
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_invalid_name(self):
        async def inner():

            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/contacts/add", json={
                    "first_name": "",
                    "last_name": None,
                    "phone_number": "+1234567894",
                    "address": "East Blue"
                })

                logging.info("Assert request failed")
                assert response.status_code == 404, f"Expected 400 for invalid name - {response.json()}"
                assert "Invalid name" in response.json()["error_msg"], "Error message should indicate invalid name."
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_same_name(self):

        async def inner():
            # setup client
            logging.info("Setting up client")
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                
                # add contact
                logging.info(f"Adding {self.zoro_other_phone} as contact")
                response = await client.post("/api/contacts/add", json=self.zoro_other_phone)
                assert response.status_code == 200, f"Failed to add user - {response.json()}"
                assert response.json() == {"status": "ok"}

                # assert add endpoint worked
                logging.info(f"Getting info from db where phone number = {self.zoro_other_phone['phone_number']}")
                async for db_conn in get_db():
                    zoro_contact = await self.get_contact_from_db(self.zoro_other_phone['phone_number'], db_conn)

                assert zoro_contact is not None, f"Contact {self.zoro_other_phone['first_name']} should exist in the database."
                assert zoro_contact.first_name == self.zoro_other_phone['first_name'], f"First name is note the same -> {zoro_contact.first_name} != {self.zoro_other_phone['first_name']}"
                assert zoro_contact.last_name == self.zoro_other_phone['last_name'], f"Last name is note the same -> {zoro_contact.last_name} != {self.zozoro_other_phonero['last_name']}"
                assert zoro_contact.phone_number == self.zoro_other_phone['phone_number'], f"Phone number is note the same -> {zoro_contact.phone_number} != {self.zoro_other_phone['phone_number']}"
                assert zoro_contact.address == self.zoro_other_phone['address'], f"Address is note the same -> {zoro_contact.address} != {self.zoro_other_phone['address']}"
                assert zoro_contact.created_ts is not None, f"created_ts is None"
                assert zoro_contact.updated_ts is not None, f"updated_ts is None"
                assert zoro_contact.deleted_ts is None, f"deleted_ts is not None"

        asyncio.get_event_loop().run_until_complete(inner())