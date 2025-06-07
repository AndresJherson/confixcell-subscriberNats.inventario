from typing import Optional
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class KardexLockOrm(SQLModel, table=True):
    __tablename__ = "kardex_lock" #type:ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(max_length=50, unique=True)
    clave: str = Field(max_length=100, unique=True)
    fecha: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))