import re

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