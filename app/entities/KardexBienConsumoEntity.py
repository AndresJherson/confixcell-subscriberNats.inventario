from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship
from app.entities.EventoPendienteKardexBienConsumoEntity import EventoPendienteKardexBienConsumoEntity
from app.entities.KardexMovimientoBienConsumoEntity import KardexMovimientoBienConsumoEntity

class KardexBienConsumoEntity(SQLModel, table=True, table_name="kardex_bien_consumo"):
    id: int = Field(sa_column=Column(primary_key=True, autoincrement=False))
    almacen_uuid: str = Field(max_length=50)
    bien_consumo_uuid: str = Field(max_length=50)
    saldo_cant: float = Field(default=0)
    saldo_valor_uni: float = Field(default=0)
    saldo_valor_tot: float = Field(default=0)

    detalles: list["KardexMovimientoBienConsumoEntity"] = Relationship(back_populates="kardex")
    eventos: list["EventoPendienteKardexBienConsumoEntity"] = Relationship(back_populates="kardex")