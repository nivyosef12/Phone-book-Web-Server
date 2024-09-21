import logging
import pytest

import app.common.utils as app_utils
class TestAppUtils: 

    @classmethod
    def setup_class(cls):
        try:
            cls.present_env_var = "ENV"
            cls.not_present_env_var = "NOT_PRESENT"
        
        except Exception as e:
            logging.error(f"Error in setting up TestAppUtils class: {e}")
            raise Exception(f"Error in setting up TestAppUtils class: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            pass
        except Exception as e:
            logging.error(f"Error in tearing down TestAppUtils class: {e}")
            raise Exception(f"Error in tearing down TestAppUtils class: {e}")
    
    def test_get_env_variable_found(self):
        """
        Test that the function correctly retrieves an environment variable when it exists.
        """
        try:
            env_val = app_utils.get_env_variable(self.present_env_var)
            assert env_val == "develop", f"Loadded different env value -> {env_val} != develop"
        except Exception as e:
            logging.error(f"test_get_env_variable_found error: {e}")
            raise e


    def test_get_env_variable_not_found_with_default(self):
        """
        Test that the function returns the default value when the environment variable is not found.
        """
        try:
            default_val = "default"
            env_val = app_utils.get_env_variable(self.not_present_env_var, default=default_val)
            assert env_val == default_val, f"Loadded different env value -> {env_val} != {default_val}"
        except Exception as e:
            logging.error(f"test_get_env_variable_found error: {e}")
            raise e



    def test_get_env_variable_not_found_without_default(self):
        """
        Test that the function raises a ValueError when the environment variable is not found
        and no default value is provided.
        """
        with pytest.raises(ValueError, match=f"Failed to get {self.not_present_env_var} from env"):
            app_utils.get_env_variable(self.not_present_env_var, default=None)
