query_bien_consumo = """
with cte_movimientos as (

    select
        
        entrada_bien_consumo.uuid as movimiento_uuid,
        null as movimiento_ref_uuid,
        'EntradaBienConsumoValorNuevo' as movimiento_tipo,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_fuente_cod_serie,
        documento_fuente.cod_numero as documento_fuente_cod_numero,
        documento_fuente.concepto as concepto,

        entrada_bien_consumo.cant as entrada_cant,
        entrada_bien_consumo_valor_nuevo.valor_uni as entrada_costo_uni,
        entrada_bien_consumo.cant * entrada_bien_consumo_valor_nuevo.valor_uni as entrada_costo_tot,

        null as salida_cant,
        null as salida_costo_uni,
        null as salida_costo_tot

    from entrada_bien_consumo_valor_nuevo
    left join entrada_bien_consumo on entrada_bien_consumo.id = entrada_bien_consumo_valor_nuevo.id
    left join documento_fuente on documento_fuente.id = entrada_bien_consumo.documento_fuente_id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null

    union all

    select
        
        entrada_bien_consumo.uuid as movimiento_uuid,
        salida_bien_consumo.uuid as movimiento_ref_uuid,
        'EntradaBienConsumoValorSalida' as movimiento_tipo,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_fuente_cod_serie,
        documento_fuente.cod_numero as documento_fuente_cod_numero,
        documento_fuente.concepto as concepto,

        entrada_bien_consumo.cant as entrada_cant,
        0 as entrada_costo_uni,
        0 as entrada_costo_tot,

        null as salida_cant,
        null as salida_costo_uni,
        null as salida_costo_tot

    from entrada_bien_consumo_valor_salida
    left join salida_bien_consumo on salida_bien_consumo.id = entrada_bien_consumo_valor_salida.salida_bien_consumo_id
    left join entrada_bien_consumo on entrada_bien_consumo.id = entrada_bien_consumo_valor_salida.id
    left join documento_fuente on documento_fuente.id = entrada_bien_consumo.documento_fuente_id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null

    union all

    select
        
        salida_bien_consumo.uuid as movimiento_uuid,
        null as movimiento_ref_uuid,
        'SalidaBienConsumoValorNuevo' as movimiento_tipo,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_fuente_cod_serie,
        documento_fuente.cod_numero as documento_fuente_cod_numero,
        documento_fuente.concepto as concepto,

        null as entrada_cant,
        null as entrada_costo_uni,
        null as entrada_costo_tot,

        salida_bien_consumo.cant as salida_cant,
        0 as salida_costo_uni,
        0 as salida_costo_tot

    from salida_bien_consumo_valor_nuevo
    left join salida_bien_consumo on salida_bien_consumo.id = salida_bien_consumo_valor_nuevo.id
    left join documento_fuente on documento_fuente.id = salida_bien_consumo.documento_fuente_id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null

    union all

    select
        
        salida_bien_consumo.uuid as movimiento_uuid,
        entrada_bien_consumo.uuid as movimiento_ref_uuid,
        'SalidaBienConsumoValorEntrada' as movimiento_tipo,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_fuente_cod_serie,
        documento_fuente.cod_numero as documento_fuente_cod_numero,
        documento_fuente.concepto as concepto,

        null as entrada_cant,
        null as entrada_costo_uni,
        null as entrada_costo_tot,

        salida_bien_consumo.cant as salida_cant,
        0 as salida_costo_uni,
        0 as salida_costo_tot

    from salida_bien_consumo_valor_entrada
    left join entrada_bien_consumo on entrada_bien_consumo.id = salida_bien_consumo_valor_entrada.entrada_bien_consumo_id
    left join salida_bien_consumo on salida_bien_consumo.id = salida_bien_consumo_valor_entrada.id
    left join documento_fuente on documento_fuente.id = salida_bien_consumo.documento_fuente_id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null

    union all

    select
        
        salida_bien_consumo.uuid as movimiento_uuid,
        null as movimiento_ref_uuid,
        'NotaVentaSalidaBienConsumo' as movimiento_tipo,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_fuente_cod_serie,
        documento_fuente.cod_numero as documento_fuente_cod_numero,
        documento_fuente.concepto as concepto,

        null as entrada_cant,
        null as entrada_costo_uni,
        null as entrada_costo_tot,

        salida_bien_consumo.cant as salida_cant,
        0 as salida_costo_uni,
        0 as salida_costo_tot

    from nv_salida_bien_consumo
    left join salida_bien_consumo on salida_bien_consumo.id = nv_salida_bien_consumo.id
    left join documento_fuente on documento_fuente.id = salida_bien_consumo.documento_fuente_id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null

    union all

    select
        
        nv_servicio_reparacion_recurso_bien_consumo.uuid as movimiento_uuid,
        null as movimiento_ref_uuid,
        'NotaVentaSalidaProduccionServicioReparacionRecursoBienConsumo' as movimiento_tipo,

        nv_servicio_reparacion_recurso_bien_consumo.fecha as fecha,
        documento_fuente.cod_serie as documento_fuente_cod_serie,
        documento_fuente.cod_numero as documento_fuente_cod_numero,
        documento_fuente.concepto as 'servicio de reparación',

        null as entrada_cant,
        null as entrada_costo_uni,
        null as entrada_costo_tot,

        nv_servicio_reparacion_recurso_bien_consumo.cant as salida_cant,
        0 as salida_costo_uni,
        0 as salida_costo_tot

    from nv_servicio_reparacion_recurso_bien_consumo
    left join nv_servicio_reparacion on nv_servicio_reparacion.id = nv_servicio_reparacion_recurso_bien_consumo.nv_servicio_reparacion_id
    left join nota_venta on nota_venta.id = nv_servicio_reparacion.nota_venta_id
    left join documento_transaccion on documento_transaccion.id = nota_venta.id
    left join documento_fuente on documento_fuente.id = documento_transaccion.id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null
)
select * from cte_movimientos
order by fecha asc;
"""