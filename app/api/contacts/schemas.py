from pydantic import BaseModel
from typing import Optional

# --------------------------------- AddContactInput ---------------------------------
class AddContactInput(BaseModel):
    first_name: str
    phone_number: str
    last_name: Optional[str] = None
    address: Optional[str] = None

# --------------------------------- GetContactByPhoneInput ---------------------------------
class GetContactByPhoneInput(BaseModel):
    phone_number: str