from dataclasses import dataclass
from typing import ClassVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Base


@dataclass
class BaseRepository:
    model: ClassVar[Type[Base]] = NotImplementedError

    _session: AsyncSession
