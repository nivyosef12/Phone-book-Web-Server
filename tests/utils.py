import random
import string

def random_string(length=8):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters  # Uppercase and lowercase letters
    return ''.join(random.choice(letters) for _ in range(length))

def random_phone_number():
    """Generate a random phone number."""
    return f"{random.randint(100000000, 999999999)}"