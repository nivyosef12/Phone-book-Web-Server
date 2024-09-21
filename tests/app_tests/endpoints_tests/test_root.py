import pytest
import logging
import asyncio

from app.main import app
from fastapi.testclient import TestClient

class TestRoot:

    @classmethod
    def setup_class(cls):
        try:
            cls.client = TestClient(app)
            
        except Exception as e:
            logging.error(f"Error in setting up TestRoot class: {e}")
            raise Exception(f"Error in setting up TestRoot class: {e}")

    @classmethod
    def teardown_class(cls):
        try:
            pass
        except Exception as e:
            logging.error(f"Error in tearing down TestRoot class: {e}")
            raise Exception(f"Error in tearing down TestRoot class: {e}")

    def test_root(self):
        response = self.client.get("/")
        res_content = response.json()
        res_code = response.status_code
        assert res_code == 200, f"Status codes are not the same. {res_code} != 200"
        assert res_content == {"message": "OK"}, f"Responses are not the same. {res_content} != {'message': 'OK'}"