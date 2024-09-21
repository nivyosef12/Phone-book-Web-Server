import logging

from fastapi import APIRouter, HTTPException, Response, status, Request, Depends
from fastapi.responses import JSONResponse, Response

headers = {
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}

router = APIRouter()

# --------------------------------- AuthorInfo ---------------------------------
from app.api.contacts.schemas import AddContactInput
from app.api.contacts.services.AddContanct import add_contact

@router.post("/add", tags=["contacts"])
async def add_contact_endpoint(add_contact_input: AddContactInput):
    logging.info(f"add_contact endpoint for {1 if add_contact_input.last_name is None else f'{add_contact_input.first_name} {add_contact_input.last_name}'} with {add_contact_input.phone_number} as phone number")

    status_code, result = await add_contact(add_contact_input.first_name, add_contact_input.phone_number, last_name=add_contact_input.last_name, address=add_contact_input.address)
    return Response(content=result, status_code=status_code, headers=headers)
    
