from pprint import pprint
from con import RouteOrder
from con import Partners
from con import lxtrack_cliente
from con import lxtrack_cliente_direccion
from con import Employee
from con import lxtrack_usuario
from con import lxtrack_reporte
from con import lxtrack_orden
from con import PosOrder
from con import PosSession
from con import ResZone
from con import PosConfig
from con import PosOrderLine
from con import lxtrack_pedido
from con import Products
from con import AccountBankStatement
from con import AccountBankStatementLine
from con import StockPicking
from con import StockMove

def main():
    pprint('Sync Lxtrack')

    #Se buscan las ordenes sin sincronizar para subirse a LXTRACK
    ordercon = RouteOrder()
    orders0 = ordercon.readNoSync()
    partnercon = Partners()
    lx_cliente = lxtrack_cliente()
    lx_cliente_direccion = lxtrack_cliente_direccion()
    lx_usuario = lxtrack_usuario()
    employeecon = Employee()
    lx_orden = lxtrack_orden()
    for order0 in orders0:
        pprint(order0['name'])
        #inserta o actualiza cliente
        partner = partnercon.read(order0['partner_id'][0])
        lx_cliente.insert(partner[0])
        #inserta o actualiza direcciones
        partnerdir = partnercon.read(order0['partner_shipping_id'][0])
        lx_cliente_direccion.insert(partnerdir[0],order0['partner_id'][0])
        #inserta o actualiza empleados
        employee = employeecon.read(order0['manage_id'][0])
        lx_usuario.insert(employee[0])
        #inserta  orden y actualiza status
        lx_orden.insert(order0)
        ordercon.update(order0['id'], { 'state': "1"} )

    #Actualiza estatus de LXTRACK
    status=lx_orden.read_status()
    for state in status:
        #pprint(state)
        ordercon.update(state['id_local'], { 'state': state['clave_orden_estatus' ] } )

    #Sube los pedidos a odoo
    lx_reporte = lxtrack_reporte()
    reportes = lx_reporte.read()
    posordercon = PosOrder()
    possessioncon = PosSession()
    zonecon = ResZone()
    posconfigcon = PosConfig()
    posorderlinecon = PosOrderLine()
    lx_pedido = lxtrack_pedido()
    accountbankstatementcon = AccountBankStatement()
    accountbankstatementlinecon = AccountBankStatementLine()
    stockpickingcon = StockPicking()
    productcon = Products()
    stockmovecon = StockMove()

    #productcon = Products()
    for reporte in reportes:
        #pprint(reporte)
        employeeroute = employeecon.read(reporte['id_usuario_creator'])
        lx_orden1 = lx_orden.read(reporte['id_orden'])
        order = ordercon.read( lx_orden1._rows[0]['id_odoo'] )
        zone = zonecon.read(order[0]['zone_id'][0])
        possession = possessioncon.read(zone[0]['pos_id'][0])
        posconfig = posconfigcon.read(zone[0]['pos_id'][0])
        #inserta movimiento de almacen
        vars = {
            'name': reporte['id_orden'],
            'location_id' : posconfig[0]['stock_location_id'][0],
            'move_type' : 'direct',
            'state' : 'done',
            'priority' : '1',
            'scheduled_date': str(reporte['ctrl_date_termino']),
            'date': str(reporte['ctrl_date_termino']),
            'date_done': str(reporte['ctrl_date_termino']),
            'location_dest_id' : '9', #automatizar
            'picking_type_id' : '9', #automatizar
            'company_id': posconfig[0]['company_id'][0],
            'is_locked' : 'true',
            'immediate_trasfer' : 'false',
            'create_uid': employeeroute[0]['user_id'][0]
        }
        stockpicking = stockpickingcon.create(vars)

        #inserta  pedio de venta
        vars = {
            'name' : 'New',
            'session_id' : possession[0]['id'],
            'date_order' : reporte['ctrl_date_termino'],
            'partner_id' : reporte['id_cliente'],
            'company_id' : posconfig[0]['company_id'][0],
            'location_id' : posconfig[0]['stock_location_id'][0],
            'user_id' : employeeroute[0]['user_id'][0],
            'pricelist_id' : posconfig[0]['pricelist_id'][0],
            'picking_id' : stockpicking,
            'pos_reference' : reporte['id_orden'],
            'sale_journal' : posconfig[0]['journal_id'][0],
            'amount_tax' : str(reporte['amount_tax']),
            'amount_total' : str(reporte['amount_total']),
            'amount_paid' : str(reporte['amount_total']),
            'amount_return' : '0',
            'create_uid' : employeeroute[0]['user_id'][0]
        }
        posorder = posordercon.read(posordercon.create(vars) )

        #Registro del pago
        vars = {
            'name' : possession[0]['name'],
            'date' : reporte['ctrl_date_termino'],
            'balance_start' : '0',
            'state' : 'open',
            'journal_id' : posconfig[0]['journal_ids'][0],
            'company_id' : posconfig[0]['company_id'][0],
            'total_entry_encoding' :  str(reporte['amount_total']),
            #'balance_start' : str(reporte['amount_total']),
            #'difference' :  str(reporte['amount_total']*-1),
            'user_id' : employeeroute[0]['user_id'][0],
            'create_uid' : employeeroute[0]['user_id'][0],
            'pos_session_id' : possession[0]['id']
        }

        accountbankstatement_id = accountbankstatementcon.create(vars)
        vars = {
            'name' : posorder[0]['name'],
            'date' : reporte['ctrl_date_termino'],
            'amount' : str(reporte['amount_total']),
            'account_id' : posconfig[0]['journal_id'][0],
            'statement_id' : accountbankstatement_id,
            'journal_id' : posconfig[0]['journal_ids'][0],
            'ref' : possession[0]['name'],
            'sequence' : '1',
            'company_id' : posconfig[0]['company_id'][0],
            'create_uid': employeeroute[0]['user_id'][0],
            'pos_statement_id' : posorder[0]['id']
        }
        accountbankstatementlinecon.create(vars)
        #Insteta linas del pedido
        pedidos = lx_pedido.read(reporte['id'])
        for pedido in pedidos:
            pprint (pedido)
            product = productcon.read(pedido['id_producto'])
            vals = {
                'company_id': posconfig[0]['company_id'][0],
                'name' : posorder[0]['name'],
                'product_id' : pedido['id_producto'],
                'price_unit' : str(pedido['precio_unitario']),
                'qty' : pedido['cantidad'],
                'price_subtotal': str(pedido['price_subtotal']),
                'price_subtotal_incl': str(pedido['price_subtotal_incl']),
                'order_id' : posorder[0]['id'],
                'create_uid' : employeeroute[0]['user_id'][0]
            }
            pprint(vals)
            posorderlinecon.create(vals)
            vars= {
                'name' : posorder[0]['name'],
                'sequence' : '10',
                'priority' : '1',
                'create_date': str(reporte['ctrl_date_termino']),
                'date': str(reporte['ctrl_date_termino']),
                'company_id': posconfig[0]['company_id'][0],
                'date_expected': str(reporte['ctrl_date_termino']),
                'product_id' : product[0]['id'],
                #'product_qty' : pedido['cantidad'],
                'product_uom_qty' : pedido['cantidad'],
                'product_uom' : product[0]['uom_id'][0],
                'location_id': posconfig[0]['stock_location_id'][0],
                'location_dest_id': '9',  # automatizar
                'picking_type_id' : '9', #automatizar
                'picking_id' : stockpicking,
                'state' : 'done',
                'price_unit' : str(pedido['price_subtotal_incl']*-1),
                'value': str(pedido['price_subtotal_incl'] * -1),
                'procure_method' : 'make_to_stock',
                'scrapped' : 'false',
                'propagate' : 'true',
                'aditional' : 'false',
                'to_refud' : 'false',
                'remaining_qty': str(pedido['cantidad']*-1),
                'remaining_value': str(pedido['price_subtotal_incl'] * -1),
            }
            stockmovecon.create(vars)
        #actualiza sync
        lx_reporte.sync(reporte['id'])

    pprint('Termina sync')


if __name__ == "__main__":
    main()