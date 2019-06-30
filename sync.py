from pprint import pprint
from con import RouteOrder
from con import Partners
from con import lxtrack_cliente
from con import lxtrack_cliente_direccion

def main():
    pprint('Sync Lxtrack')

    #Se buscan las ordenes sin sincronizar
    ordercon = RouteOrder()
    orders0 = ordercon.read(0)
    partnercon = Partners()
    lx_cliente = lxtrack_cliente()
    lx_cliente_direccion = lxtrack_cliente_direccion()
    for order0 in orders0:
        pprint(order0['name'])
        #inserta o actualiza cliente
        partner = partnercon.read(order0['partner_id'][0])
        lx_cliente.insert(partner[0])
        #inserta o actualiza direcciones
        partnerdir = partnercon.read(order0['partner_shipping_id'][0])
        lx_cliente_direccion.insert(partnerdir[0],order0['partner_id'][0])
        #inseta o actualiza dirección



    pprint('Termina sync')


if __name__ == "__main__":
    main()