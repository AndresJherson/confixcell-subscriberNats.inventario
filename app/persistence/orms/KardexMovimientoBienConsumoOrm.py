from decimal import Decimal
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class KardexMovimientoBienConsumoOrm(SQLModel, table=True):
    __tablename__ = "kardex_movimiento_bien_consumo" #type:ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(max_length=50, unique=True)
    kardex_bien_consumo_id: int = Field(foreign_key='kardex_bien_consumo.id')
    movimiento_uuid: str = Field(max_length=50, unique=True)
    movimiento_ref_uuid: Optional[str] = Field(default_factory=lambda:None, max_length=50)
    movimiento_tipo: str = Field(max_length=100)
    fecha: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    documento_fuente_cod_serie: str = Field(max_length=50)
    documento_fuente_cod_numero: int
    concepto: Optional[str] = Field(default_factory=lambda:None, max_length=100)
    entrada_cant: Optional[Decimal] = Field(default_factory=lambda:None, decimal_places=2, max_digits=22)
    entrada_costo_uni: Optional[Decimal] = Field(default_factory=lambda:None, decimal_places=2, max_digits=22)
    entrada_costo_tot: Optional[Decimal] = Field(default_factory=lambda:None, decimal_places=2, max_digits=22)
    entrada_cant_acumulado: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    entrada_costo_acumulado: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    salida_cant: Optional[Decimal] = Field(default_factory=lambda:None, decimal_places=2, max_digits=22)
    salida_costo_uni: Optional[Decimal] = Field(default_factory=lambda:None, decimal_places=2, max_digits=22)
    salida_costo_tot: Optional[Decimal] = Field(default_factory=lambda:None, decimal_places=2, max_digits=22)
    salida_cant_acumulado: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    salida_costo_acumulado: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_cant: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_valor_uni: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)
    saldo_valor_tot: Decimal = Field(default_factory=lambda:Decimal('0'), decimal_places=2, max_digits=22)