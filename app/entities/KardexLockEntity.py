from sqlalchemy import Column
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class KardexLockEntity(SQLModel, table=True, table_name="kardex_lock"):
    clave: str = Field(sa_column=Column(primary_key=True, autoincrement=False), max_length=100)
    fecha: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))