from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import TEXT, Column, DateTime
from sqlmodel import Field, SQLModel

class ErrorKardexBienConsumoOrm(SQLModel, table=True):
    __tablename__ = "error_kardex_bien_consumo" #type:ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(max_length=50, unique=True)
    kardex_bien_consumo_id: int = Field(foreign_key="kardex_bien_consumo.id")
    fecha: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))
    mensaje: str = Field(sa_type=TEXT)