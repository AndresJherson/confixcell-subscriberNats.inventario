from typing import Optional
from pydantic import BaseModel

from app.domain.dtos.KardexBienConsumoDTO import KardexBienConsumoDTO

class WrapperKardexBienConsumoDTO(BaseModel):
    crear: Optional[dict[str, "KardexBienConsumoDTO"]] = None
    eliminar: Optional[dict[str, "KardexBienConsumoDTO"]] = None