from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlalchemy import TEXT, Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.entities import KardexBienConsumoEntity


class ErrorKardexBienConsumoEntity(SQLModel, table=True, table_name="error_kardex_bien_consumo"):
    
    id: Optional[int] = Field(default_factory=lambda:None, primary_key=True)
    kardex_bien_consumo_id: int = Field(foreign_key="kardex_bien_consumo.id")
    fecha: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))
    mensaje: str = Field(sa_type=TEXT)
    
    # Relación
    kardex_bien_consumo: Optional["KardexBienConsumoEntity"] = Relationship(back_populates="errores")