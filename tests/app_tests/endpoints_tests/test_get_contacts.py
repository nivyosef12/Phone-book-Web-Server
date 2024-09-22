# import httpx
# import asyncio
# import logging
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from app.main import app
# from app.api.contacts.models import Contact
# from app.common.db import get_db
# from tests.utils import random_phone_number, random_string
# import pytest

# class TestGetContact:

#     @classmethod
#     async def setup_class(cls):
#         cls.number_of_contacts = 15
#         phone_numbers = set()
#         cls.contacts = []
#         async for db_conn in get_db():
#             for i in range(cls.number_of_contacts):
#                 # Generate unique phone number
#                 phone_number = random_phone_number()
#                 while phone_number in phone_numbers:
#                     phone_number = random_phone_number()
#                 phone_numbers.add(phone_number)

#                 new_contact = Contact(
#                     first_name=random_string(), 
#                     last_name=random_string(),
#                     phone_number=phone_number, 
#                     address=random_string()
#                 )
#                 db_conn.add(new_contact)

#             await db_conn.commit()

#     @pytest.mark.asyncio
#     async def test_add_contact_success(self):
#         # Setup client
#         async with httpx.AsyncClient(app=app, base_url="http://test") as client:
#             # Add contact
#             response = await client.get(f"/api/contacts/get_contact/?limit=9&offset=0")
#             assert response.status_code == 200, f"Failed to get contacts - {response.json()}"
