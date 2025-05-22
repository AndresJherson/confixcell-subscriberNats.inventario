from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class KardexLockEntity(SQLModel, table=True, table_name="kardex_lock"):
    
    clave: str = Field(primary_key=True, max_length=100)
    fecha: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))