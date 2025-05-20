from datetime import datetime, timezone
from typing import Any, Optional
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel
from app.entities.KardexBienConsumoEntity import KardexBienConsumoEntity


class EventoPendienteKardexBienConsumoEntity(SQLModel, table=True, table_name="evento_pendiente_kardex_bien_consumo"):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    kardex_bien_consumo_id: int = Field(foreign_key="kardex_bien_consumo.id")
    evento: str = Field(max_length=100)
    data: dict[str, Any] = Field(sa_type=JSON)
    fecha: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

    kardex_bien_consumo: "KardexBienConsumoEntity" = Relationship(back_populates="eventos_pendientes")