import pytest
import httpx
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

    async def get_contact_from_db(self, phone_number, db_conn: AsyncSession):
        result = await db_conn.execute(
            select(Contact).where(Contact.phone_number == phone_number)
        )
        return result.scalars().first()

    @pytest.mark.asyncio
    async def test_add_contact_success(self):
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

    # TODO add more tests