from sqlmodel import SQLModel, Field, Relationship
from app.entities.KardexMovimientoBienConsumoEntity import KardexMovimientoBienConsumoEntity

class KardexBienConsumoEntity(SQLModel, table=True):
    id: int = Field(primary_key=True)
    almacen_uuid: str = Field(max_length=50)
    bien_consumo_uuid: str = Field(max_length=50)
    saldo_cant: float = Field(default=0)
    saldo_valor_uni: float = Field(default=0)
    saldo_valor_tot: float = Field(default=0)

    detalles: list["KardexMovimientoBienConsumoEntity"] = Relationship(back_populates="kardex")