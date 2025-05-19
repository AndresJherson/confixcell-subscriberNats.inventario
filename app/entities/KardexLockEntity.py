from sqlmodel import SQLModel, Field
from datetime import datetime

class KardexLockEntity(SQLModel, table=True):
    clave: str = Field(primary_key=True)
    fecha: datetime = Field(default_factory=datetime.utcnow)