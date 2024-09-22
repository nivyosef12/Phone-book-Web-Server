import logging

from fastapi import APIRouter, HTTPException, Response, Query, Request, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.db import get_db

headers = {
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}

router = APIRouter()

# --------------------------------- AddContact ---------------------------------
from app.api.contacts.schemas import AddContactInput
from app.api.contacts.services.AddContanct import add_contact

@router.post("/add", tags=["contact"])
async def add_contact_endpoint(add_contact_input: AddContactInput, db_conn: AsyncSession = Depends(get_db)):
    # TODO add logs for time metrics
    full_name = f"{add_contact_input.first_name}" if add_contact_input.last_name is None else f"{add_contact_input.first_name} {add_contact_input.last_name}"
    logging.info(f"add_contact endpoint for {full_name} with {add_contact_input.phone_number} as phone number")

    try:
        async with db_conn.begin():
            status_code, result = await add_contact(db_conn, add_contact_input.first_name, add_contact_input.phone_number, last_name=add_contact_input.last_name, address=add_contact_input.address)
    except Exception as e:
        logging.error(f"Faild to add {full_name} to DB. {e}")
        await db_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Faild to add {full_name} to DB. {e}")
        
    return Response(content=result, status_code=status_code, headers=headers)
 
# --------------------------------- GetAllContacts ---------------------------------
from app.api.contacts.schemas import GetAllContacts
from app.api.contacts.services.GetContact import get_all_contancts

@router.get("/get_contant/", tags=["contact"])
async def get_contact_endpoint(input_data: GetAllContacts = Depends(), db_conn: AsyncSession = Depends(get_db)):
    # TODO add logs for time metrics

    try:
        async with db_conn.begin():
            status_code, result = await get_all_contancts(db_conn, input_data.limit, input_data.offset)
    except Exception as e:
        await db_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Faild to get contants from DB - {e}")
        
    return Response(content=result, status_code=status_code, headers=headers)
    

# --------------------------------- GetContactByPhone ---------------------------------
from app.api.contacts.schemas import GetContactByPhoneInput
from app.api.contacts.services.GetContact import get_contanct_by_phone

@router.get("/get_contant/by_phone/", tags=["contact"])
async def get_contact_endpoint(input_data: GetContactByPhoneInput = Depends(), db_conn: AsyncSession = Depends(get_db)):
    # TODO add logs for time metrics

    try:
        async with db_conn.begin():
            status_code, result = await get_contanct_by_phone(db_conn, input_data.phone_number)
    except Exception as e:
        await db_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Faild to get contant from DB - {e}")
        
    return Response(content=result, status_code=status_code, headers=headers)

