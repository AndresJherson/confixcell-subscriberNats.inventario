from datetime import datetime, timezone
import json
from typing import Any
from app.domain.dtos.WrapperKardexBienConsumoDTO import WrapperKardexBienConsumoDTO


if __name__ == "__main__":
    dic: dict[str, Any] = {
        'crear': {
            '1': {
                'almacen': {
                    'uuid': '123123123'
                },
                'bienConsumo': {
                    'uuid': 'asdfasdfasdf'
                },
                'movimientos': []
            },
            '2': {
                'almacen': {
                    'uuid': '321321'
                },
                'bienConsumo': {
                    'uuid': 'fdsafdsa'
                },
                'movimientos': [
                    {
                        'movimientoUuid': 'qqq',
                        'movimientoTipo': 'mitipo',
                        'fecha': '2025-04-15 08:15:45.000 -05:00',
                        'documentoFuenteCodigoSerie': 'serieA',
                        'documentoFuenteCodigoNumero': 3,
                        'entradaCantidad': 23.3432,
                        'entradaCostoUnitarios': 982.465
                    }
                ]
            }
        }
    }

    # fe = datetime.fromisoformat('2025-04-15 08:15:45.000 -05:00')
    # print(fe)
    dto = WrapperKardexBienConsumoDTO(**dic)
    dto = dto.model_dump_json()
    dto = WrapperKardexBienConsumoDTO(**json.loads(dto))
    print(dto)
    print(datetime.now(timezone.utc))