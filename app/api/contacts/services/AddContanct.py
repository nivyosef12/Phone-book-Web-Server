import logging
import json

async def add_contact(first_name, phone_number, last_name=None, address=None):
    # TODO check input
    # insert to db

    return 200, json.dumps({"status": "ok"})