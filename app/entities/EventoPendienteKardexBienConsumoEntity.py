from datetime import datetime
from typing import Any
from sqlmodel import Field, SQLModel


class EventoPendienteKardexBienConsumoEntity(SQLModel, table=True):
    id: int = Field(primary_key=True)
    kardex_bien_consumo_id: int = Field(foreign_key="kardexbienconsumo.id")
    evento: str
    data: dict[Any, Any]
    fecha: datetime = Field(default_factory=datetime.utcnow)