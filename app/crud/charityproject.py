from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


PROJECT_TIMEDIFF_FIELD = 'timediff'


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        return (await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )).scalars().first()

    async def get_project_invested_amount(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> int:
        project_invested_amount = await session.execute(
            select(CharityProject.invested_amount).where(
                CharityProject.id == project_id
            )
        )
        return project_invested_amount.scalars().first()

    async def get_project_fully_invested(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> bool:
        project_fully_invested = await session.execute(
            select(CharityProject.fully_invested).where(
                CharityProject.id == project_id
            )
        )
        return project_fully_invested.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )
        return sorted(
            projects.scalars().all(),
            key=lambda obj: obj.close_date - obj.create_date
        )


charityproject_crud = CRUDCharityProject(CharityProject)
