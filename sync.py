from pprint import pprint
from con import RouteOrder
from con import Partners
from con import lxtrack_cliente
from con import lxtrack_cliente_direccion
from con import Employee
from con import lxtrack_usuario
from con import lxtrack_orden

def main():
    pprint('Sync Lxtrack')

    #Se buscan las ordenes sin sincronizar
    ordercon = RouteOrder()
    orders0 = ordercon.read(0)
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




    pprint('Termina sync')


if __name__ == "__main__":
    main()