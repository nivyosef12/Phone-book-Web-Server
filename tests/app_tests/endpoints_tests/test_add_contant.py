import httpx
import asyncio

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
        cls.sunji = {
            "first_name": "Sunji",
            "phone_number": "invalid_phone",
            "address": "East Blue"
        }
        cls.ussop = {
            "first_name": "Ussop",
            "phone_number": "+1234567893"
        }

    async def get_contact_from_db(self, phone_number, db_conn: AsyncSession):
        result = await db_conn.execute(
            select(Contact).where(Contact.phone_number == phone_number)
        )
        return result.scalars().first()

    def test_add_contact_success(self):

        async def inner():
            # Setup the client
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                
                # Add the contact
                response = await client.post("/api/contacts/add", json=self.luffy)
                assert response.status_code == 200, f"Failed to add user - {response.json()}"
                assert response.json() == {"status": "ok"}

                # Obtain the database session using async for
                async for db_conn in get_db():
                    luffy_contact = await self.get_contact_from_db(self.luffy['phone_number'], db_conn)

                # Assert contact in db
                assert luffy_contact is not None, "Contact should exist in the database."
                assert luffy_contact.address == self.luffy['address'], "Address does not match."
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_missing_first_name(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/contacts/add", json={
                    "phone_number": "+1234567892",
                    "address": "East Blue"
                })
                assert response.status_code == 422, f"Expected 422 for missing first name - {response.json()}"
        asyncio.get_event_loop().run_until_complete(inner())
        
    def test_add_contact_invalid_phone_number(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/contacts/add", json=self.sunji)

                assert response.status_code == 404, f"Expected 400 for invalid phone number - {response.json()}"
                assert "Invalid phone number" in response.json()["error_msg"], "Error message should indicate invalid phone number."
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_duplicate_phone_number(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                # First add Luffy contact
                await client.post("/api/contacts/add", json=self.luffy)

                # Attempt to add Luffy again
                response = await client.post("/api/contacts/add", json=self.luffy)
                assert response.status_code == 400, f"Expected 400 for duplicate phone number - {response.json()}"
                assert "Integrity Error" in response.json()["error_msg"], "Error message should indicate duplicate entry."
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_without_address(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/contacts/add", json=self.ussop)
                assert response.status_code == 200, f"Failed to add user without address - {response.json()}"
                assert response.json() == {"status": "ok"}

                # Verify the contact was added without an address
                async for db_conn in get_db():
                    usopp_contact = await self.get_contact_from_db(self.ussop['phone_number'], db_conn)
                
                assert usopp_contact is not None, "Contact should exist in the database."
                assert usopp_contact.address is None, "Address should be None."
        asyncio.get_event_loop().run_until_complete(inner())

    def test_add_contact_invalid_name(self):
        async def inner():
            async with httpx.AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/contacts/add", json={
                    "first_name": "",
                    "last_name": None,
                    "phone_number": "+1234567894",
                    "address": "East Blue"
                })
                assert response.status_code == 404, f"Expected 400 for invalid name - {response.json()}"
                assert "Invalid name" in response.json()["error_msg"], "Error message should indicate invalid name."
        asyncio.get_event_loop().run_until_complete(inner())