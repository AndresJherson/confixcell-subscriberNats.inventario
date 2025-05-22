from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.entities import ErrorKardexBienConsumoEntity
    from app.entities import EventoPendienteKardexBienConsumoEntity
    from app.entities import KardexMovimientoBienConsumoEntity

class KardexBienConsumoEntity(SQLModel, table=True, table_name="kardex_bien_consumo"):

    id: Optional[int] = Field(default_factory=lambda:None, primary_key=True)
    almacen_uuid: str = Field(max_length=50)
    bien_consumo_uuid: str = Field(max_length=50)
    entrada_cant: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    entrada_costo_uni: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    entrada_costo_tot: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    salida_cant: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    salida_costo_uni: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    salida_costo_tot: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_cant: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_valor_uni: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_valor_tot: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    
    # Relaciones
    movimientos: list["KardexMovimientoBienConsumoEntity"] = Relationship(back_populates="kardex_bien_consumo")
    eventos_pendientes: list["EventoPendienteKardexBienConsumoEntity"] = Relationship(back_populates="kardex_bien_consumo")
    errores: list["ErrorKardexBienConsumoEntity"] = Relationship(back_populates="kardex_bien_consumo")