from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    first_name_lower = Column(String(100))
    last_name = Column(String(100))
    last_name_lower = Column(String(100))
    phone_number = Column(String(15), unique=True)
    address = Column(Text)
    created_ts = Column(TIMESTAMP, server_default=func.now())
    updated_ts = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deleted_ts = Column(TIMESTAMP, nullable=True)