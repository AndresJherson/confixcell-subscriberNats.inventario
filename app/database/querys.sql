use confixcell_documentos_fuente;

-- entrada_bien_consumo
select
    
    entrada_bien_consumo.uuid as movimiento_uuid,
    null as movimiento_ref_uuid,

    documento_fuente.f_emision as fecha,
    documento_fuente.cod_serie as documento_cod_serie,
    documento_fuente.cod_numero as documento_cod_numero,
    documento_fuente.concepto as concepto,

    entrada_bien_consumo.cant as entrada_cantidad,
    entrada_bien_consumo_valor_nuevo.valor_uni as entrada_costo_uni,
    entrada_bien_consumo.cant * entrada_bien_consumo_valor_nuevo.valor_uni as entrada_costo_tot,

    null as salida_cantidad,
    null as salida_costo_uni,
    null as salida_costo_tot

from entrada_bien_consumo_valor_nuevo
left join entrada_bien_consumo on entrada_bien_consumo.id = entrada_bien_consumo_valor_nuevo.id
left join documento_fuente on documento_fuente.id = entrada_bien_consumo.documento_fuente_id
where documento_fuente.f_emision is not null
and documento_fuente.f_anulacion is null
and entrada_bien_consumo.almacen_uuid = ''
and entrada_bien_consumo.bien_consumo_uuid = ''

union all

-- entrada_bien_consumo_valor_salida
select
    
    entrada_bien_consumo.uuid as movimiento_uuid,
    salida_bien_consumo.uuid as movimiento_ref_uuid,

    documento_fuente.f_emision as fecha,
    documento_fuente.cod_serie as documento_cod_serie,
    documento_fuente.cod_numero as documento_cod_numero,
    documento_fuente.concepto as concepto,

    entrada_bien_consumo.cant as entrada_cantidad,
    0 as entrada_costo_uni,
    0 as entrada_costo_tot,

    null as salida_cantidad,
    null as salida_costo_uni,
    null as salida_costo_tot

from entrada_bien_consumo_valor_salida
left join salida_bien_consumo on salida_bien_consumo.id = entrada_bien_consumo_valor_salida.salida_bien_consumo_id
left join entrada_bien_consumo on entrada_bien_consumo.id = entrada_bien_consumo_valor_salida.id
left join documento_fuente on documento_fuente.id = entrada_bien_consumo.documento_fuente_id
where documento_fuente.f_emision is not null
and documento_fuente.f_anulacion is null
and entrada_bien_consumo.almacen_uuid = ''
and entrada_bien_consumo.bien_consumo_uuid = ''

union all

-- salida_bien_consumo_valor_nuevo
select
    
    salida_bien_consumo.uuid as movimiento_uuid,
    null as movimiento_ref_uuid,

    documento_fuente.f_emision as fecha,
    documento_fuente.cod_serie as documento_cod_serie,
    documento_fuente.cod_numero as documento_cod_numero,
    documento_fuente.concepto as concepto,

    null as entrada_cantidad,
    null as entrada_costo_uni,
    null as entrada_costo_tot,

    salida_bien_consumo.cant as salida_cantidad,
    0 as salida_costo_uni,
    0 as salida_costo_tot

from salida_bien_consumo_valor_nuevo
left join salida_bien_consumo on salida_bien_consumo.id = salida_bien_consumo_valor_nuevo.id
left join documento_fuente on documento_fuente.id = salida_bien_consumo.documento_fuente_id
where documento_fuente.f_emision is not null
and documento_fuente.f_anulacion is null
and salida_bien_consumo.almacen_uuid = ''
and salida_bien_consumo.bien_consumo_uuid = ''

union all

-- salida_bien_consumo_valor_entrada
select
    
    salida_bien_consumo.uuid as movimiento_uuid,
    entrada_bien_consumo.uuid as movimiento_ref_uuid,

    documento_fuente.f_emision as fecha,
    documento_fuente.cod_serie as documento_cod_serie,
    documento_fuente.cod_numero as documento_cod_numero,
    documento_fuente.concepto as concepto,

    null as entrada_cantidad,
    null as entrada_costo_uni,
    null as entrada_costo_tot,

    salida_bien_consumo.cant as salida_cantidad,
    0 as salida_costo_uni,
    0 as salida_costo_tot

from salida_bien_consumo_valor_entrada
left join entrada_bien_consumo on entrada_bien_consumo.id = salida_bien_consumo_valor_entrada.entrada_bien_consumo_id
left join salida_bien_consumo on salida_bien_consumo.id = salida_bien_consumo_valor_entrada.id
left join documento_fuente on documento_fuente.id = salida_bien_consumo.documento_fuente_id
where documento_fuente.f_emision is not null
and documento_fuente.f_anulacion is null
and salida_bien_consumo.almacen_uuid = ''
and salida_bien_consumo.bien_consumo_uuid = ''

union all

-- nv_salida_bien_consumo
select
    
    salida_bien_consumo.uuid as movimiento_uuid,
    null as movimiento_ref_uuid,

    documento_fuente.f_emision as fecha,
    documento_fuente.cod_serie as documento_cod_serie,
    documento_fuente.cod_numero as documento_cod_numero,
    documento_fuente.concepto as concepto,

    null as entrada_cantidad,
    null as entrada_costo_uni,
    null as entrada_costo_tot,

    salida_bien_consumo.cant as salida_cantidad,
    0 as salida_costo_uni,
    0 as salida_costo_tot

from nv_salida_bien_consumo
left join salida_bien_consumo on salida_bien_consumo.id = nv_salida_bien_consumo.id
left join documento_fuente on documento_fuente.id = salida_bien_consumo.documento_fuente_id
where documento_fuente.f_emision is not null
and documento_fuente.f_anulacion is null
and salida_bien_consumo.almacen_uuid = ''
and salida_bien_consumo.bien_consumo_uuid = ''

union all

-- nv_servicio_reparacion_recurso_bien_consumo
select
    
    nv_servicio_reparacion_recurso_bien_consumo.uuid as movimiento_uuid,
    null as movimiento_ref_uuid,

    nv_servicio_reparacion_recurso_bien_consumo.fecha as fecha,
    documento_fuente.cod_serie as documento_cod_serie,
    documento_fuente.cod_numero as documento_cod_numero,
    documento_fuente.concepto as 'servicio de reparación',

    null as entrada_cantidad,
    null as entrada_costo_uni,
    null as entrada_costo_tot,

    nv_servicio_reparacion_recurso_bien_consumo.cant as salida_cantidad,
    0 as salida_costo_uni,
    0 as salida_costo_tot

from nv_servicio_reparacion_recurso_bien_consumo
left join nv_servicio_reparacion on nv_servicio_reparacion.id = nv_servicio_reparacion_recurso_bien_consumo.nv_servicio_reparacion_id
left join nota_venta on nota_venta.id = nv_servicio_reparacion.nota_venta_id
left join documento_transaccion on documento_transaccion.id = nota_venta.id
left join documento_fuente on documento_fuente.id = documento_transaccion.id
where documento_fuente.f_emision is not null
and documento_fuente.f_anulacion is null
and nv_servicio_reparacion_recurso_bien_consumo.almacen_uuid = ''
and nv_servicio_reparacion_recurso_bien_consumo.bien_consumo_uuid = '';





with cte_movimientos as (

    select
        
        entrada_bien_consumo.id as movimiento_id,
        entrada_bien_consumo.uuid as movimiento_uuid,
        null as movimiento_ref_uuid,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_cod_serie,
        documento_fuente.cod_numero as documento_cod_numero,
        documento_fuente.concepto as concepto,

        entrada_bien_consumo.cant as entrada_cantidad,
        entrada_bien_consumo_valor_nuevo.valor_uni as entrada_costo_uni,
        entrada_bien_consumo.cant * entrada_bien_consumo_valor_nuevo.valor_uni as entrada_costo_tot,

        null as salida_cantidad,
        null as salida_costo_uni,
        null as salida_costo_tot

    from entrada_bien_consumo_valor_nuevo
    left join entrada_bien_consumo on entrada_bien_consumo.id = entrada_bien_consumo_valor_nuevo.id
    left join documento_fuente on documento_fuente.id = entrada_bien_consumo.documento_fuente_id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null

    union all

    select
        
        entrada_bien_consumo.id as movimiento_id,
        entrada_bien_consumo.uuid as movimiento_uuid,
        salida_bien_consumo.uuid as movimiento_ref_uuid,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_cod_serie,
        documento_fuente.cod_numero as documento_cod_numero,
        documento_fuente.concepto as concepto,

        entrada_bien_consumo.cant as entrada_cantidad,
        0 as entrada_costo_uni,
        0 as entrada_costo_tot,

        null as salida_cantidad,
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
        
        salida_bien_consumo.id as movimiento_id,
        salida_bien_consumo.uuid as movimiento_uuid,
        null as movimiento_ref_uuid,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_cod_serie,
        documento_fuente.cod_numero as documento_cod_numero,
        documento_fuente.concepto as concepto,

        null as entrada_cantidad,
        null as entrada_costo_uni,
        null as entrada_costo_tot,

        salida_bien_consumo.cant as salida_cantidad,
        0 as salida_costo_uni,
        0 as salida_costo_tot

    from salida_bien_consumo_valor_nuevo
    left join salida_bien_consumo on salida_bien_consumo.id = salida_bien_consumo_valor_nuevo.id
    left join documento_fuente on documento_fuente.id = salida_bien_consumo.documento_fuente_id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null

    union all

    select
        
        salida_bien_consumo.id as movimiento_id,
        salida_bien_consumo.uuid as movimiento_uuid,
        entrada_bien_consumo.uuid as movimiento_ref_uuid,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_cod_serie,
        documento_fuente.cod_numero as documento_cod_numero,
        documento_fuente.concepto as concepto,

        null as entrada_cantidad,
        null as entrada_costo_uni,
        null as entrada_costo_tot,

        salida_bien_consumo.cant as salida_cantidad,
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
        
        salida_bien_consumo.id as movimiento_id,
        salida_bien_consumo.uuid as movimiento_uuid,
        null as movimiento_ref_uuid,

        documento_fuente.f_emision as fecha,
        documento_fuente.cod_serie as documento_cod_serie,
        documento_fuente.cod_numero as documento_cod_numero,
        documento_fuente.concepto as concepto,

        null as entrada_cantidad,
        null as entrada_costo_uni,
        null as entrada_costo_tot,

        salida_bien_consumo.cant as salida_cantidad,
        0 as salida_costo_uni,
        0 as salida_costo_tot

    from nv_salida_bien_consumo
    left join salida_bien_consumo on salida_bien_consumo.id = nv_salida_bien_consumo.id
    left join documento_fuente on documento_fuente.id = salida_bien_consumo.documento_fuente_id
    where documento_fuente.f_emision is not null
    and documento_fuente.f_anulacion is null

    union all

    select
        
        nv_servicio_reparacion_recurso_bien_consumo.id as movimiento_id,
        nv_servicio_reparacion_recurso_bien_consumo.uuid as movimiento_uuid,
        null as movimiento_ref_uuid,

        nv_servicio_reparacion_recurso_bien_consumo.fecha as fecha,
        documento_fuente.cod_serie as documento_cod_serie,
        documento_fuente.cod_numero as documento_cod_numero,
        documento_fuente.concepto as 'servicio de reparación',

        null as entrada_cantidad,
        null as entrada_costo_uni,
        null as entrada_costo_tot,

        nv_servicio_reparacion_recurso_bien_consumo.cant as salida_cantidad,
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
order by fecha asc, movimiento_id asc;