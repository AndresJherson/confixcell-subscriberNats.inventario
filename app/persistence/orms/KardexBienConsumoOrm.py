from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field

   
class KardexBienConsumoOrm(SQLModel, table=True):
    __tablename__ = "kardex_bien_consumo" #type:ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(max_length=50, unique=True)
    almacen_uuid: str = Field(max_length=50)
    bien_consumo_uuid: str = Field(max_length=50)
    entrada_cant_acumulado: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    entrada_costo_acumulado: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    salida_cant_acumulado: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    salida_costo_acumulado: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_cant: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_valor_uni: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_valor_tot: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    f_creacion: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))
    f_actualizacion: datetime = Field(default_factory=lambda:datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True)))