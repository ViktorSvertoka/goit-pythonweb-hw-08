from datetime import date
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import Date

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(50))
    phone = Column(String(50))
    birthday = Column(Date, nullable=False)
    notes = Column(String(300), nullable=True)
