from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(40), nullable=False)
    email = Column(String(50), unique=True, index=True)
    phone = Column(Integer, unique=True, index=True)
    birthday = Column(Date)