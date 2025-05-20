from datetime import datetime, timezone
from typing import Any, Optional
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from app.entities.KardexBienConsumoEntity import KardexBienConsumoEntity


class EventoPendienteKardexBienConsumoEntity(SQLModel, table=True, table_name="evento_pendiente_kardex_bien_consumo"):
    id: int = Field(sa_column=Column(primary_key=True, autoincrement=False))
    kardex_bien_consumo_id: int = Field(foreign_key="kardex_bien_consumo.id")
    evento: str
    data: dict[Any, Any]
    fecha: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    
    kardex: Optional["KardexBienConsumoEntity"] = Relationship(back_populates="eventos")