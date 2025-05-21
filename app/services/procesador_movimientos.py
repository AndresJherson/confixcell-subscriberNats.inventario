from decimal import Decimal
from typing import Hashable
from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.MovimientoTipoBienConsumo import MovimientoTipoBienConsumo

class ProcesadorMovimientos:
    
    def __init__(self, session: AsyncSession, df: DataFrame, saldo_cant: Decimal, saldo_valor_uni: Decimal, saldo_valor_tot: Decimal):
        self.session = session
        self.df = df
        self.saldo_cant = saldo_cant
        self.saldo_valor_uni = saldo_valor_uni
        self.saldo_valor_tot = saldo_valor_tot
        
    def set_df(self, df: DataFrame):
        self.df = df
        
    def procesar(self):
        for index, row in self.df.iterrows():
            
            match row["movimiento_tipo"]:
        
                case MovimientoTipoBienConsumo.ENTRADA_VALOR_NUEVO.value:
                    self.procesar_entrada_valor_nuevo(index)
                    
                case MovimientoTipoBienConsumo.ENTRADA_VALOR_SALIDA.value:
                    self.procesar_entrada_valor_salida(index)
                        
                case MovimientoTipoBienConsumo.SALIDA_VALOR_NUEVO.value:
                    self.procesar_salida_valor_nuevo(index)
                    
                case MovimientoTipoBienConsumo.SALIDA_VALOR_ENTRADA.value:
                    self.procesar_salida_valor_entrada(index)
                    
                case MovimientoTipoBienConsumo.SALIDA_NOTA_VENTA.value:
                    self.procesar_salida_nota_venta(index)
                    
                case MovimientoTipoBienConsumo.SALIDA_NOTA_VENTA_SERVICIO_REPARACION_RECURSO.value:
                    self.procesar_salida_nota_venta_servicio_reparacion_recurso(index)
                    
                case _:
                    continue

    def procesar_entrada_valor_nuevo(self, index: Hashable):
        pass

    def procesar_entrada_valor_salida(self, index: Hashable):
        pass

    def procesar_salida_valor_nuevo(self, index: Hashable):
        pass

    def procesar_salida_valor_entrada(self, index: Hashable):
        pass

    def procesar_salida_nota_venta(self, index: Hashable):
        pass

    def procesar_salida_nota_venta_servicio_reparacion_recurso(self, index: Hashable):
        pass
    
    
    def actualizar_tabla_movimientos(self):
        # reemplazar los movimientos actualizados a la db
        pass