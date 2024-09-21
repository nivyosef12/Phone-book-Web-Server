from pydantic import BaseModel

# --------------------------------- AddContactInput ---------------------------------
class AddContactInput(BaseModel):
    first_name: str
    phone_number: str
    last_name: str = None
    address: str = None

# --------------------------------- GetContactByPhoneInput ---------------------------------
class GetContactByPhoneInput(BaseModel):
    phone_number: str