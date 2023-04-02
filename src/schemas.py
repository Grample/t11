from datetime import date
from pydantic import BaseModel, Field, EmailStr

class ContactBase(BaseModel):
    first_name: str = Field("John", max_length=50)
    last_name: str = Field("Smith", max_length=50)
    email: EmailStr
    phone: int = Field("111", gt=100, le=99999999999)
    birthday: date

class ContactModel(ContactBase):
    pass

class ContactUpdate(ContactModel):
    pass

class ContactResponse(ContactBase):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: int
    birthday: date
    
    class Config:
        orm_mode = True