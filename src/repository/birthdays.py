from datetime import timedelta, datetime
from typing import List
from sqlalchemy import select
from sqlalchemy.sql import extract
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate


class BirthdayRepository:

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int, daygap: int) -> List[Contact]:

        today = datetime.now()
        start_day = today.timetuple().tm_yday
        end_day = (today + timedelta(days=daygap)).timetuple().tm_yday

        if end_day < start_day:
            stmt = (
                select(Contact)
                .filter(
                    (extract("doy", Contact.birthday) >= start_day)
                    | (extract("doy", Contact.birthday) <= end_day)
                )
                .offset(skip)
                .limit(limit)
            )
        else:
            stmt = (
                select(Contact)
                .filter(extract("doy", Contact.birthday).between(start_day, end_day))
                .offset(skip)
                .limit(limit)
            )

        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()
