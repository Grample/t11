from typing import List
from datetime import datetime, timedelta
from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def get_contacts_by_fname(first_name: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(func.lower(Contact.first_name).like(f'%{first_name.lower()}%')).all()

async def get_contacts_by_lname(last_name: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(func.lower(Contact.last_name).like(f'%{last_name.lower()}%')).all()

async def get_contacts_by_email(email: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.email.like(f'%{email}%')).all()

async def get_contacts_by_birthday(db: Session) -> List[Contact]:
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).filter(and_(extract('month', Contact.birthday) == next_week.month,
                                             extract('day', Contact.birthday) <= next_week.day,
                                             extract('day', Contact.birthday) >= today.day,
                                             )).all()
    birthday_contacts = []
    for contact in contacts:
        bday_this_year = contact.birthday.replace(year=today.year)
        if bday_this_year >= today:
            birthday_contacts.append(contact)
    return birthday_contacts

async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone=body.phone,
                      birthday=body.birthday)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact

async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact