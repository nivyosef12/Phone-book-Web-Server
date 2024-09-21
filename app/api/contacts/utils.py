import re

def is_valid_phone_number(phone_number):
    if phone_number is None:
        return False
    
    pattern = re.compile(r'^\+?\d{10,15}$')
    return bool(pattern.match(phone_number))

def is_valid_name(first_name, last_name):
    if first_name is None:
        return False
    
    pattern = re.compile(r"^[A-Za-z\s\-']{1,100}$")
    return bool(pattern.match(first_name)) and bool(pattern.match(last_name) if last_name is not None else True)