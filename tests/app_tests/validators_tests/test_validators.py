import logging
import pytest

from app.api.contacts.utils import validate_name, validate_phone

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
    
    
    def test_validate_name(self):
        """
        Test the validate_name function for valid and invalid cases.
        """
        # valid cases
        assert validate_name("John")
        assert validate_name("Jane Doe")
        assert validate_name("O Connor")
        
        # invalid cases
        with pytest.raises(ValueError, match="Name must contain only letters and spaces"):
            validate_name("John123")

        with pytest.raises(ValueError, match="Name must contain only letters and spaces"):
            validate_name("Jane@Doe")

        with pytest.raises(ValueError, match="Name must contain only letters and spaces"):
            validate_name(" ")
        
        with pytest.raises(ValueError, match="Name must contain only letters and spaces"):
            validate_name("")

        assert validate_name(None) is None 

    def test_validate_phone(self):
        """
        Test the validate_phone function for valid and invalid cases.
        """
        # valid cases
        assert validate_phone("+1234567890")
        assert validate_phone("1234567890")
        assert validate_phone("+12345678901234")  # maximum of 15 digits including '+'
        
        # invalid cases
        with pytest.raises(ValueError, match="Phone number must contain only digits and optionally start with '\\+'"):
            validate_phone("")

        with pytest.raises(ValueError, match="Phone number must contain only digits and optionally start with '\\+'"):
            validate_phone(" ")

        with pytest.raises(ValueError, match="Phone number must contain only digits and optionally start with '\\+'"):
            validate_phone("1234567890123456")

        with pytest.raises(ValueError, match="Phone number must contain only digits and optionally start with '\\+'"):
            validate_phone("+123abc7890")

        with pytest.raises(ValueError, match="Phone number must contain only digits and optionally start with '\\+'"):
            validate_phone("123-456-7890")
        
        with pytest.raises(ValueError, match="Phone number must contain only digits and optionally start with '\\+'"):
            validate_phone("1234 56789")
        
        assert validate_phone(None) is None