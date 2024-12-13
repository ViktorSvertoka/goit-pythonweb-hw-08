from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.birthdays import BirthdayRepository
from src.schemas import ContactModel


class BirthdayService:
    def __init__(self, db: AsyncSession):
        self.repository = BirthdayRepository(db)

    async def get_contacts(self, skip: int, limit: int, daygap: int):
        return await self.repository.get_contacts(skip, limit, daygap)
