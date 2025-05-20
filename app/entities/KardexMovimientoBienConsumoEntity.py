from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from app.entities.KardexBienConsumoEntity import KardexBienConsumoEntity

class KardexMovimientoBienConsumoEntity(SQLModel, table=True, table_name="kardex_movimiento_bien_consumo"):
    id: int = Field(sa_column=Column(primary_key=True, autoincrement=False))
    kardex_bien_consumo_id: int = Field(foreign_key="kardex_bien_consumo.id")
    movimiento_uuid: str = Field(max_length=50, unique=True)
    movimiento_ref_uuid: Optional[str] = Field(default=None)
    movimiento_tipo: str = Field(max_length=100)
    fecha: datetime
    documento_fuente_cod_serie: str = Field(max_length=50)
    documento_fuente_cod_numero: int
    concepto: Optional[str] = Field(max_length=100, default=None)
    entrada_cant: Optional[float] = None
    entrada_costo_uni: Optional[float] = None
    entrada_costo_tot: Optional[float] = None
    salida_cant: Optional[float] = None
    salida_costo_uni: Optional[float] = None
    salida_costo_tot: Optional[float] = None
    saldo_cant: float = Field(default=0)
    saldo_valor_uni: float = Field(default=0)
    saldo_valor_tot: float = Field(default=0)

    kardex: Optional["KardexBienConsumoEntity"] = Relationship(back_populates="detalles")