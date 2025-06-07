from pydantic import BaseModel

from app.domain.dtos.AlmacenDTO import AlmacenDTO
from app.domain.dtos.BienConsumoDTO import BienConsumoDTO
from app.domain.dtos.KardexMovimientoBienConsumoDTO import KardexMovimientoBienConsumoDTO

class KardexBienConsumoDTO(BaseModel):
    almacen: "AlmacenDTO"
    bienConsumo: "BienConsumoDTO"
    movimientos: list["KardexMovimientoBienConsumoDTO"]