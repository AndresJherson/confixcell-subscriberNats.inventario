from datetime import datetime
from decimal import Decimal
from typing import Any, Optional
import dateutil
import dateutil.parser
from pydantic import BaseModel, field_validator


class KardexMovimientoBienConsumoDTO(BaseModel):
    movimientoUuid: str
    movimientoRefUuid: Optional[str] = None
    movimientoTipo: str
    fecha: datetime
    documentoFuenteCodigoSerie: str
    documentoFuenteCodigoNumero: int
    concepto: Optional[str] = None
    entradaCantidad: Optional[Decimal] = None
    entradaCostoUnitario: Optional[Decimal] = None
    entradaCostoTotal: Optional[Decimal] = None
    salidaCantidad: Optional[Decimal] = None
    salidaCostoUnitario: Optional[Decimal] = None
    salidaCostoTotal: Optional[Decimal] = None
    
    @field_validator('fecha', mode='before')
    @classmethod
    def parse_datetime(cls, v: Any):
        if isinstance(v, str):
            return dateutil.parser.parse(v)
        return v
    