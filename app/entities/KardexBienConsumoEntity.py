from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.entities.EventoPendienteKardexBienConsumoEntity import EventoPendienteKardexBienConsumoEntity
from app.entities.KardexMovimientoBienConsumoEntity import KardexMovimientoBienConsumoEntity

class KardexBienConsumoEntity(SQLModel, table=True, table_name="kardex_bien_consumo"):

    id: Optional[int] = Field(default=None, primary_key=True)
    almacen_uuid: str = Field(max_length=50)
    bien_consumo_uuid: str = Field(max_length=50)
    saldo_cant: Decimal = Field(default=0)
    saldo_valor_uni: Decimal = Field(default=0)
    saldo_valor_tot: Decimal = Field(default=0)

    movimientos: list["KardexMovimientoBienConsumoEntity"] = Relationship(
        back_populates="kardex", 
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    eventos_pendientes: list["EventoPendienteKardexBienConsumoEntity"] = Relationship(
        back_populates="kardex",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )