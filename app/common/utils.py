import os
import json
import urllib3

from app.common.logger import logger

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.common.exceptions import ConflictError, RecordNotFound

def handle_exception(e):
    """
        Helper function to handles errors form the server.

        Args:
            e (Exception): the exception that was raises
            
        Returns:
            proper error code and error message
    """
    if isinstance(e, ValueError):
        error_code = 404
        error_message = f"Value Error: {e}"
    elif isinstance(e, RecordNotFound):
        error_code = 404
        error_message = f"Record Not Found Error: {e}"
    elif isinstance(e, urllib3.exceptions.HTTPError):
        error_code = 400
        error_message = f"HTTP Error: {e}"
    elif isinstance(e, IntegrityError):
        error_code = 400
        error_message = f"Integrity Error: {e}"
    elif isinstance(e, ConflictError):
        error_code = 409
        error_message = f"Conflict Error: {e}"
    elif isinstance(e, HTTPException):
        error_code = e.status_code
        error_message = e.detail
    else:
        error_code = 500
        error_message = f"Internal Error: {str(e)}"

    log_msg = f"Error - {error_message}"
    logger.error(log_msg, exc_info=False)
    return error_code, json.dumps({"error_msg": log_msg})

def get_env_variable(var_name, default=None):
    """
        Retrieves the value of an environment variable.

        If the environment variable is not found and no default value is provided, 
        a `ValueError` is raised.

        Args:
            var_name (str): The name of the environment variable to retrieve.
            default (Any, optional): The value to return if the environment variable is not found. 
                                    If `None` is provided and the environment variable is not found, 
                                    a `ValueError` will be raised. Defaults to None.

        Returns:
            Any: The value of the environment variable, or the default value if the variable is not set.

        Raises:
            ValueError: If the environment variable is not found and no default value is provided.
    """
    logger.info(f"Getting env var - {var_name}")
    var_value = os.environ.get(var_name, None)

    # if None - needs to load env for the first time
    try:
        if var_value is None:
            logger.info(f"Didnt found {var_name}, loading .env file")
            load_dotenv()

            var_value = os.environ.get(var_name, default)
    except Exception as e:
        log_msg = f"Faild to load .env file - {e}"
        logger.error(log_msg, exc_info=True)
        raise Exception(log_msg)
    
    # no value found and no default argument given
    if var_value is None:
        raise ValueError(f"Failed to get {var_name} from env")
    return var_value

    

