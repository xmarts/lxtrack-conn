from con import Products
from con import Pricelist
from con import lxtrack_lista_precios
from con import lxtrack_cat_producto
from con import lxtrack_precios
from con import ProductPricelist
from pprint import pprint

def main():
    pprint('Importacion de catalogos')

    #Catalogo prodcutos lxtrack_cat_producto
    productcon = Products()
    products = productcon.read()
    cat_producto = lxtrack_cat_producto()
    for product in products:
        #inserta productos
        pprint(product['name'])
        cat_producto.insert(product)

    #Catalogo de listas de precios
    lista_precioscon = Pricelist()
    lista_precios = lista_precioscon.read()
    lx_listaprecios = lxtrack_lista_precios()

    for lista in lista_precios:
        ##inserta precios
        lx_listaprecios.insert(lista)
        print(lista['name'])

    #Catalogo de lista de precios
    precioscon = ProductPricelist()
    precios = precioscon.read()
    lx_precios = lxtrack_precios()

    for precio in precios:
        ##inserta precios
        lx_precios.insert(precio)
        print(precio['id'])



    pprint('Termina importación')


if __name__ == "__main__":
    main()