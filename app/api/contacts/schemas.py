from pydantic import BaseModel
from typing import Optional

# --------------------------------- AddContactInput ---------------------------------
class AddContactInput(BaseModel):
    first_name: str
    phone_number: str
    last_name: Optional[str] = None
    address: Optional[str] = None

# --------------------------------- GetContactByPhoneInput ---------------------------------
class GetAllContacts(BaseModel):
    limit: int
    offset: Optional[int] = 0

# --------------------------------- GetContactByPhoneInput ---------------------------------
class GetContactByPhoneInput(BaseModel):
    phone_number: str

# --------------------------------- EditContactInput ---------------------------------
class EditContactInput(BaseModel):
    phone_number: str
    new_phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None

# --------------------------------- DeleteContactInput ---------------------------------
class DeleteContactInput(BaseModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# --------------------------------- SearchContactInput ---------------------------------
class SearchContactInput(BaseModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None