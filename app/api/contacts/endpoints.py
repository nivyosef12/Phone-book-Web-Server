import json

from fastapi import APIRouter, HTTPException, Response, Query, Request, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.db import get_db
from app.common.logger import logger


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
    logger.info(f"add_contact endpoint for {add_contact_input}")

    try:
        async with db_conn.begin():
            status_code, result = await add_contact(db_conn, add_contact_input)
    except Exception as e:
        logger.error(f"Faild to add {full_name} to DB. {e}")
        await db_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Faild to add {full_name} to DB. {e}")
        
    return Response(content=result, status_code=status_code, headers=headers)
 
# --------------------------------- GetAllContacts ---------------------------------
from app.api.contacts.schemas import GetAllContacts
from app.api.contacts.services.GetContact import get_all_contancts

@router.get("/get", tags=["contact"])
async def get_contact_endpoint(input_data: GetAllContacts = Depends(), db_conn: AsyncSession = Depends(get_db)):
    logger.info(f"get_contact endpoint for {input_data}")

    try:
        async with db_conn.begin():
            status_code, result = await get_all_contancts(db_conn, input_data)
    except Exception as e:
        await db_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Faild to get contants from DB - {e}")
        
    return Response(content=result, status_code=status_code, headers=headers)
    

# --------------------------------- EditContact ---------------------------------
from app.api.contacts.schemas import EditContactInput
from app.api.contacts.services.EditContact import edit_contact

@router.post("/edit", tags=["contact"])
async def edit_contact_endpoint(edit_contact_input: EditContactInput, db_conn: AsyncSession = Depends(get_db)):
    # TODO add logs for time metrics
    logger.info(f"edit_contant endpoint for {edit_contact_input} called")

    if isinstance(edit_contact_input.phone_number, ValueError) or isinstance(edit_contact_input.first_name, ValueError) or isinstance(edit_contact_input.last_name, ValueError):
        return Response(content=json.dumps({"status": "error", "message": "Unprocessable Entity"}), status_code=422, headers=headers)

    if edit_contact_input.new_phone_number is None and edit_contact_input.first_name is None and edit_contact_input.last_name is None and edit_contact_input.address is None:
         return Response(content=json.dumps({"status": "error", "message": "At least one edit criteria must be provided."}), status_code=422, headers=headers)
    try:
        async with db_conn.begin():
            status_code, result = await edit_contact(db_conn, edit_contact_input)
    except Exception as e:
        logger.error(f"Faild to edit {edit_contact_input.phone_number}. {e}")
        await db_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Faild to edit {edit_contact_input.phone_number}. {e}")
        
    return Response(content=result, status_code=status_code, headers=headers)


# --------------------------------- DeleteContact ---------------------------------
from app.api.contacts.schemas import DeleteContactInput
from app.api.contacts.services.DeleteContact import delete_contact

@router.post("/delete", tags=["contact"])
async def delete_contact_endpoint(delete_contact_input: DeleteContactInput, db_conn: AsyncSession = Depends(get_db)):
    # TODO add logs for time metrics
    logger.info(f"add_contant endpoint for {delete_contact_input} called")

    if delete_contact_input.phone_number is None and delete_contact_input.first_name is None and delete_contact_input.last_name is None:
         return Response(content=json.dumps({"status": "error", "message": "At least one delete criteria must be provided."}), status_code=422, headers=headers)
    try:
        async with db_conn.begin():
            status_code, result = await delete_contact(db_conn, delete_contact_input)
    except Exception as e:
        logger.error(f"Faild to delete {delete_contact_input.phone_number}. {e}")
        await db_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Faild to delete {delete_contact_input.phone_number}. {e}")
        
    return Response(content=result, status_code=status_code, headers=headers)


# --------------------------------- SearchContactInput ---------------------------------
from app.api.contacts.schemas import SearchContactInput
from app.api.contacts.services.SearchContact import search_contact

@router.get("/search", tags=["contact"])
async def search_contact_endpoint(search_contact_input: SearchContactInput = Depends(), db_conn: AsyncSession = Depends(get_db)):
    # TODO add logs for time metrics
    logger.info(f"searchcontant endpoint for {search_contact_input} called")

    if isinstance(search_contact_input.phone_number, ValueError) or isinstance(search_contact_input.first_name, ValueError) or isinstance(search_contact_input.last_name, ValueError):
        return Response(content=json.dumps({"status": "error", "message": "Unprocessable Entity"}), status_code=422, headers=headers)

    if search_contact_input.phone_number is None and search_contact_input.first_name is None and search_contact_input.last_name is None:
        return Response(content=json.dumps({"status": "error", "message": "At least one search criteria must be provided."}), status_code=400, headers=headers)
    
    try:
        async with db_conn.begin():
            status_code, result = await search_contact(db_conn, search_contact_input)
    except Exception as e:
        logger.error(f"Faild to search {search_contact_input.phone_number}. {e}")
        await db_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Faild to search {search_contact_input.phone_number}. {e}")
        
    return Response(content=result, status_code=status_code, headers=headers)