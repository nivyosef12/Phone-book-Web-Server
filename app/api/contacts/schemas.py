from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional
from app.common.utils import get_env_variable
from app.api.contacts.utils import validate_name, validate_phone

# --------------------------------- AddContactInput ---------------------------------
class AddContactInput(BaseModel):
    first_name: str = Field(..., max_length=100)
    phone_number: str = Field(..., max_length=15)
    last_name: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None

    @field_validator('*')
    def validate_fields(cls, v, info: ValidationInfo) -> Optional[str]:
        if info.field_name in ['first_name', 'last_name']:
            return validate_name(v)
        elif info.field_name == 'phone_number':
            return validate_phone(v)
        return v

# --------------------------------- GetAllContacts ---------------------------------
class GetAllContacts(BaseModel):
    limit: int = Field(..., gt=1, lt=int(get_env_variable("LIMIT_CONTACTS_RESPONSE"))+1)
    offset: Optional[int] = Field(0, ge=0)

# --------------------------------- EditContactInput ---------------------------------
class EditContactInput(BaseModel):
    phone_number: str = Field(..., max_length=15)
    new_phone_number: Optional[str] = Field(None, max_length=15)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None

    @field_validator('*')
    def validate_fields(cls, v, info: ValidationInfo) -> Optional[str]:
        if info.field_name in ['first_name', 'last_name']:
            return validate_name(v)
        elif info.field_name in ['phone_number', 'new_phone_number']:
            return validate_phone(v)

        # check if at least one field is being edited
        if info.field_name == list(info.data.keys())[-1]:
            edit_fields = {'new_phone_number', 'first_name', 'last_name', 'address'}
            if not any(info.data.get(f) for f in edit_fields):
                raise ValueError("At least one field must be provided for editing")

        return v

# --------------------------------- DeleteContactInput ---------------------------------
class DeleteContactInput(BaseModel):
    phone_number: Optional[str] = Field(None, max_length=15)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)

    @field_validator('*')
    def validate_fields(cls, v, info: ValidationInfo) -> Optional[str]:
        if info.field_name in ['first_name', 'last_name']:
            return validate_name(v)
        elif info.field_name == 'phone_number':
            return validate_phone(v)

        # check if at least one field is provided
        if info.field_name == list(info.data.keys())[-1] and not any(info.data.values()):
            raise ValueError("At least one field must be provided")

        return v

# --------------------------------- SearchContactInput ---------------------------------
class SearchContactInput(BaseModel):
    phone_number: Optional[str] = Field(None, max_length=15)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)

    @field_validator('phone_number')
    def validate_phone(cls, v) -> Optional[str]:
        try:
            validate_phone(v)
            return v
        except:
            return ValueError("Phone number must contain only digits and optionally start with '+'")
    
    @field_validator('first_name', 'last_name')
    def validate_name(cls, v) -> Optional[str]:
            try:
                validate_name(v)
                return v
            except:
                return ValueError("Name must contain only letters and spaces") 