from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from datetime import date, timedelta
from src.database.connect_db import get_db
from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get(
    "/",
    response_model=List[ContactResponse]
)
async def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contacts

@router.get(
    "/by_id/{contact_id}",
    response_model=ContactResponse
)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contact

@router.get(
    "/by_fname/{first_name}",
    response_model=List[ContactResponse]
)
async def get_contacts_by_fname(first_name: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_fname(first_name, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contacts

@router.get(
    "/by_lname/{last_name}",
    response_model=List[ContactResponse]
)
async def get_contacts_by_lname(last_name: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_lname(last_name, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contacts

@router.get(
    "/by_email/{email}",
    response_model=List[ContactResponse])
async def get_contacts_by_email(email: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_email(email, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contacts

@router.post(
    "/",
    response_model=ContactResponse
)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)

@router.put(
    "/{contact_id}",
    response_model=ContactResponse
)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contact

@router.delete(
    "/{contact_id}",
    response_model=ContactResponse
)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    return contact