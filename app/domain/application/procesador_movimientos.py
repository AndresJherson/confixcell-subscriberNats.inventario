from decimal import ROUND_HALF_UP, Decimal, getcontext
from typing import Hashable
from pandas import DataFrame

from app.domain.models.MovimientoTipoBienConsumo import MovimientoTipoBienConsumo
from app.persistence.orms.KardexMovimientoBienConsumoOrm import KardexMovimientoBienConsumoOrm

class ProcesadorMovimientos:
    
    def __init__(self, df: DataFrame, ultimo_movimiento: KardexMovimientoBienConsumoOrm):
        getcontext().rounding = ROUND_HALF_UP
        self.precision = Decimal('0.01')
        self.df = df
        
        self.entrada_cant_acumulado = ultimo_movimiento.entrada_cant_acumulado
        self.entrada_costo_acumulado = ultimo_movimiento.entrada_costo_acumulado
        self.salida_cant_acumulado = ultimo_movimiento.salida_cant_acumulado
        self.salida_costo_acumulado = ultimo_movimiento.salida_costo_acumulado
        self.saldo_cant = ultimo_movimiento.saldo_cant
        self.saldo_valor_uni = ultimo_movimiento.saldo_valor_uni
        self.saldo_valor_tot = ultimo_movimiento.saldo_valor_tot
        
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
        self.entrada_cant_acumulado += self.df.at[index, 'entrada_cant']
        self.entrada_costo_acumulado += self.df.at[index, 'entrada_costo_tot']
        
        self.saldo_cant += self.df.at[index, 'entrada_cant']
        self.saldo_valor_tot += self.df.at[index, 'entrada_costo_tot']
        self.establecer_saldos(index)


    def procesar_entrada_valor_salida(self, index: Hashable):
        movimiento_ref_uuid = self.df.at[index, 'movimiento_ref_uuid']
        movimiento_referenciado = self.df[self.df['movimiento_uuid'] == movimiento_ref_uuid]
        
        entrada_costo_uni = Decimal('0.0')
        if not movimiento_referenciado.empty:
            # Obtener el costo unitario de la salida original
            entrada_costo_uni = movimiento_referenciado['salida_costo_uni'].iloc[0]
            
        # Asignar el costo unitario y calcular el costo total de entrada
        self.df.at[index, 'entrada_costo_uni'] = entrada_costo_uni.quantize(self.precision)
        self.df.at[index, 'entrada_costo_tot'] = ( entrada_costo_uni * self.df.at[index, 'entrada_cant'] ).quantize(self.precision)
        
        # Actualizar los acumuladores de entrada
        self.entrada_cant_acumulado += self.df.at[index, 'entrada_cant']
        self.entrada_costo_acumulado += self.df.at[index, 'entrada_costo_tot']
        
        # Actualizar los saldos
        self.saldo_cant += self.df.at[index, 'entrada_cant']
        self.saldo_valor_tot += self.df.at[index, 'entrada_costo_tot']
        self.establecer_saldos(index)
        

    def procesar_salida_valor_nuevo(self, index: Hashable):
        self.df.at[index, 'salida_costo_uni'] = self.saldo_valor_uni.quantize(self.precision)
        self.df.at[index, 'salida_costo_tot'] = ( self.saldo_valor_uni * self.df.at[index, 'salida_cant'] ).quantize(self.precision)
        
        self.salida_cant_acumulado += self.df.at[index,'salida_cant']
        self.salida_costo_acumulado += self.df.at[index,'salida_costo_tot']
        
        self.saldo_cant -= self.df.at[index,'salida_cant']
        self.saldo_valor_tot -= self.df.at[index, 'salida_costo_tot']
        self.establecer_saldos(index)


    def procesar_salida_valor_entrada(self, index: Hashable):
        # Buscar el movimiento de entrada referenciado
        movimiento_ref_uuid = self.df.at[index, 'movimiento_ref_uuid']
        movimiento_referenciado = self.df[self.df['movimiento_uuid'] == movimiento_ref_uuid]
        
        salida_costo_uni = Decimal('0.0')
        if not movimiento_referenciado.empty:
            # Obtener el costo unitario de la entrada original
            salida_costo_uni = movimiento_referenciado['entrada_costo_uni'].iloc[0]
            
        # Asignar el costo unitario y calcular el costo total de salida
        self.df.at[index, 'salida_costo_uni'] = salida_costo_uni.quantize(self.precision)
        self.df.at[index, 'salida_costo_tot'] = ( salida_costo_uni * self.df.at[index, 'salida_cant'] ).quantize(self.precision)
        
        # Actualizar los acumuladores de salida
        self.salida_cant_acumulado += self.df.at[index, 'salida_cant']
        self.salida_costo_acumulado += self.df.at[index, 'salida_costo_tot']
        
        # Actualizar los saldos
        self.saldo_cant -= self.df.at[index, 'salida_cant']
        self.saldo_valor_tot -= self.df.at[index, 'salida_costo_tot']
        self.establecer_saldos(index)


    def procesar_salida_nota_venta(self, index: Hashable):
        pass


    def procesar_salida_nota_venta_servicio_reparacion_recurso(self, index: Hashable):
        pass

    
    def establecer_saldos(self, index: Hashable):
        self.df.at[index, 'entrada_cant_acumulado'] = self.entrada_cant_acumulado
        self.df.at[index, 'entrada_costo_acumulado'] = self.entrada_costo_acumulado
        
        self.df.at[index, 'salida_cant_acumulado'] = self.salida_cant_acumulado
        self.df.at[index, 'salida_costo_acumulado'] = self.salida_costo_acumulado
        
        try:
            self.saldo_valor_uni = self.saldo_valor_tot / self.saldo_cant
        except:
            self.saldo_valor_uni = Decimal('0.0')
            
        self.df.at[index, 'saldo_cant'] = self.saldo_cant.quantize(self.precision)
        self.df.at[index, 'saldo_valor_uni'] = self.saldo_valor_uni.quantize(self.precision)
        self.df.at[index, 'saldo_valor_tot'] = self.saldo_valor_tot.quantize(self.precision)
