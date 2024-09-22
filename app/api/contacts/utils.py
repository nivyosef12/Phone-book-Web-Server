import re
from app.common.utils import get_env_variable

def is_valid_phone_number(phone_number):
    """
        Check if a phone number is valid

        Args:
            phone_number (str): The phone number the check

        Returns:
            True iff phone number is valid
    """
    if phone_number is None:
        return False
    
    pattern = re.compile(r'^\+?\d{10,15}$')
    return bool(pattern.match(phone_number))

def is_valid_name(first_name, last_name):
    """
        Check if a given name is valid

        Args:
            first_name (str): person first name
            last_name (str): person last name

        Returns:
            True iff (first_name last_name) is a valid name
    """
    if first_name is None:
        return False
    
    pattern = re.compile(r"^[A-Za-z\s\-']{1,100}$")
    return bool(pattern.match(first_name)) and bool(pattern.match(last_name) if last_name is not None else True)

def is_valid_limit_n_offset(limit, offset):
    """
        Check if a given limit offset are valid

        Args:
            limit (int): limit with a max value of LIMIT_CONTACTS_RESPONSE env var
            offset (int): offset to skip results

        Returns:
            True iff limit and offset are valid
    """
    if not isinstance(limit, int) or not isinstance(offset, int):
        return False
    
    max_limit = int(get_env_variable("LIMIT_CONTACTS_RESPONSE", 10))

    return (limit > 0 and limit <= max_limit) and offset >= 0