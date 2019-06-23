from con import Products
from con import lxtrack_cat_producto
from con import ProductPricelist
from pprint import pprint

def main():
    pprint('Importación de catalogos')

    #Catalogo prodcutos lxtrack_cat_producto
    #productcon = Products()
    #products = productcon.read()
    #cat_producto = lxtrack_cat_producto()
    #for product in products:
    #    #inserta productos
    #    pprint(product['name'])
   #     cat_producto.insert(product)

    #Catalogo de listas de precios
    lista_precioscon = ProductPricelist()
    #lista_precios = lista_precioscon.read()

    #for precio in lista_precios:
    #    print(precio['id'])

    pprint('Termina importación')


if __name__ == "__main__":
    main()