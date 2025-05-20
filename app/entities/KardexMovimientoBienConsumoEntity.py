from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from app.entities.KardexBienConsumoEntity import KardexBienConsumoEntity

class KardexMovimientoBienConsumoEntity(SQLModel, table=True, table_name="kardex_movimiento_bien_consumo"):   

    id: Optional[int] = Field(default=None, primary_key=True)
    kardex_bien_consumo_id: int = Field(foreign_key="kardex_bien_consumo.id")
    movimiento_uuid: str = Field(max_length=50, unique=True)
    movimiento_ref_uuid: Optional[str] = Field(default=None, max_length=50)
    movimiento_tipo: str = Field(max_length=100)
    fecha: datetime
    documento_fuente_cod_serie: str = Field(max_length=50)
    documento_fuente_cod_numero: int
    concepto: Optional[str] = Field(default=None, max_length=100)
    entrada_cant: Optional[Decimal] = Field(default=None)
    entrada_costo_uni: Optional[Decimal] = Field(default=None)
    entrada_costo_tot: Optional[Decimal] = Field(default=None)
    salida_cant: Optional[Decimal] = Field(default=None)
    salida_costo_uni: Optional[Decimal] = Field(default=None)
    salida_costo_tot: Optional[Decimal] = Field(default=None)
    saldo_cant: Decimal = Field(default=0)
    saldo_valor_uni: Decimal = Field(default=0)
    saldo_valor_tot: Decimal = Field(default=0)

    kardex: "KardexBienConsumoEntity" = Relationship(back_populates="movimientos")