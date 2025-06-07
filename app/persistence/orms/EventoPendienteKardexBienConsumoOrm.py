from datetime import datetime, timezone
from typing import Any, Optional
from sqlalchemy import JSON, Column, DateTime
from sqlmodel import Field, SQLModel


class EventoPendienteKardexBienConsumoOrm(SQLModel, table=True):
    __tablename__ = "evento_pendiente_kardex_bien_consumo" #type:ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(max_length=50, unique=True)
    kardex_bien_consumo_id: int = Field(foreign_key="kardex_bien_consumo.id")
    evento: str = Field(max_length=100)
    data: dict[str, Any] = Field(sa_type=JSON)
    fecha: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))