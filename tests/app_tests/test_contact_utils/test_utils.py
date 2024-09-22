import logging
import pytest

from app.api.contacts.utils import is_valid_phone_number, is_valid_name
class TestContactUtils: 

    @classmethod
    def setup_class(cls):
        try:
            pass
        
        except Exception as e:
            logging.error(f"Error in setting up TestContactUtils class: {e}")
            raise Exception(f"Error in setting up TestContactUtils class: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            pass
        except Exception as e:
            logging.error(f"Error in tearing down TestContactUtils class: {e}")
            raise Exception(f"Error in tearing down TestContactUtils class: {e}")
    
    def test_is_valid_phone_number(self):
        """
        Test that the function correctly retrieves an environment variable when it exists.
        """
        assert (is_valid_phone_number("+1234567890"))
        assert (is_valid_phone_number("1234567890"))
        assert (is_valid_phone_number("+123456789012345"))
        
        # Invalid cases
        assert not(is_valid_phone_number(None))
        assert not(is_valid_phone_number("12345"))
        assert not(is_valid_phone_number("1234567890123456"))
        assert not(is_valid_phone_number("+123abc7890"))
        assert not(is_valid_phone_number("123-456-7890"))


    def test_is_valid_name(self):
        """
        Test that the function returns the default value when the environment variable is not found.
        """
        # Valid cases
        assert (is_valid_name("John", "Doe"))
        assert (is_valid_name("Jane", "O'Connor"))
        assert (is_valid_name("Mary-Jane", "Smith"))
        assert (is_valid_name("Alice", None))
        
        # Invalid cases
        assert not(is_valid_name(None, None))
        assert not(is_valid_name(None, "Doe"))
        assert not(is_valid_name("John123", "Doe"))
        assert not(is_valid_name("John", "Doe!"))
        assert not(is_valid_name("A" * 101, "Doe"))
        assert not(is_valid_name("John", "D" * 101))


