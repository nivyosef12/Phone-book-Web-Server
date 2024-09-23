import re
from typing import Optional

# validators
def validate_name(value: Optional[str]) -> Optional[str]:
    if value is not None:
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        return value
    return value

def validate_phone(value: Optional[str]) -> Optional[str]:
    if value == "":
        raise ValueError("Phone number must contain only digits and optionally start with '+'")
     
    if value is not None:
        if not re.match(r'^\+?\d{1,14}$', value):
            raise ValueError("Phone number must contain only digits and optionally start with '+'")
    return value