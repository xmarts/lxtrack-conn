import xmlrpc.client
import pymysql



from pprint import pprint

#conexion odoo
url = 'https://corporativo-humano-de-alto-rendimiento-tracking-461164.dev.odoo.com'
db = 'corporativo-humano-de-alto-rendimiento-tracking-461164'
username = 'admin'
password = 'admin'
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
#pprint(common.version())

#conexion mysql
myconn = pymysql.connect(host='127.0.0.1',
                             user='LX_xmartsOdoo',
                             password='rojee3SibedeSo2I',
                             db='LX_JAROCHITO',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class Products():
    def read(self):
        # Read product
        model_name = 'product.template'
        partner_ids = models.execute_kw(db, uid, password, model_name, 'search',
                                        [[['rental', '=', False]]]) #,{'limit': 10})
        partner_records = models.execute_kw(db, uid, password, model_name, 'read', [partner_ids])
        return partner_records

class Pricelist():
    def read(self):
        # Read Pricelist
        model_name = 'product.pricelist';
        ids = models.execute_kw(db, uid, password, model_name , 'search',
                                        [[['active', '=', 'true']]])  # ,{'limit': 10})
        records = models.execute_kw(db, uid, password, model_name, 'read', [ids])
        return records

class ProductPricelist():
    def read(self):
        # Read ProductsPricelist
        model_name = 'product.pricelist.item';
        ids = models.execute_kw(db, uid, password, model_name , 'search',
                                        [[['base', '=', 'list_price']]])  # ,{'limit': 10})
        records = models.execute_kw(db, uid, password, model_name, 'read', [ids])
        return records

class Partners():
    def read(self):
        # Read customers
        model_name = 'res.partner'
        partner_ids = models.execute_kw(db, uid, password, model_name, 'search',
                                        [[['customer', '=', True]]]) #,{'limit': 10})
        partner_records = models.execute_kw(db, uid, password, model_name, 'read', [partner_ids])
        return partner_records

    def create(self):
        # Create customer
        model_name = 'res.partner'
        vals = {
            'name': "New Customer",
        }
        new_id = models.execute_kw(db, uid, password, model_name, 'create', [vals])
        return new_id

    def update(self, id):
        # Update customer
        model_name = 'res.partner'
        models.execute_kw(db, uid, password, model_name, 'write', [[id], {
            'name': "Newer partner"
        }])




class lx_price():
    def read(self):
        # Read customers
        model_name = 'product_pricelist_item'
        partner_ids = models.execute_kw(db, uid, password, model_name, 'search', [[['customer', '=', True]]])
        partner_records = models.execute_kw(db, uid, password, model_name, 'read', [partner_ids])
        return partner_records


class lxtrack_cat_producto():
    def insert(self,product):
        cursor = myconn.cursor()
        try:
            query = "INSERT INTO LX_JAROCHITO.lxtrack_cat_producto  " \
                    " (id, codigo, descripcion, unidad, precio_unitario, sku, prod_type, favorito," \
                    " img_file, permite_negativos, active, insert_date, mod_date, id_usuario_creator, id_usuario_last_editor, id_local)  " \
                    " VALUES(%s, %s, %s, 1 , '0' , %s , 'P', '0', " \
                    " '', '0', '1', %s, %s , 0, 0, %s) " \
                    " ON DUPLICATE KEY UPDATE  codigo = %s  , descripcion = %s , sku = %s," \
                    " insert_date = %s , mod_date  = %s, id_local  = %s "

            args = (product['id'],product['default_code'],product['name'],product['default_code'],
                    product['create_date'],product['write_date'],product['id'],
                    product['default_code'], product['name'], product['default_code'],
                    product['create_date'], product['write_date'], product['id'])

            cursor.execute(query,args)
            myconn.commit()


        except pymysql.Error as e:
            print("Error lxtrack_cat_producto %d: %s" % (e.args[0], e.args[1]))
            return False

        finally:
            cursor.close()


class lxtrack_lista_precios():
    def insert(self,data):
        cursor = myconn.cursor()
        try:
            query = "INSERT INTO lxtrack_lista_precios " \
                        " (id, descripcion, active, insert_date, mod_date, id_usuario_creator, id_usuario_last_editor) " \
                        " VALUES(%s, %s, '1', %s, %s, 0, 0) " \
                        " ON DUPLICATE KEY UPDATE  descripcion = %s  , mod_date = %s "
            args = (data['id'],data['name'],data['create_date'],data['write_date'],data['name'],data['write_date'])
            cursor.execute(query,args)
            myconn.commit()

        except pymysql.Error as e:
            print("Error lxtrack_cat_producto %d: %s" % (e.args[0], e.args[1]))
            return False

        finally:
            cursor.close()


class lxtrack_precios():
    def insert(self,data):
        cursor = myconn.cursor()
        try:
            query = "INSERT INTO LX_JAROCHITO.lxtrack_precios " \
                    " (id, id_lista_precios, id_cat_producto, precio_unitario, active, insert_date, mod_date, id_usuario_creator, id_usuario_last_editor) " \
                    " VALUES(%s, %s, 19, %s, '1', %s, %s, 0, 0) " \
                    " ON DUPLICATE KEY UPDATE id_lista_precios  = %s  , precio_unitario = %s "
            args = (data['id'],data['pricelist_id'][0],data['fixed_price'],data['create_date'],data['write_date'],data['pricelist_id'][0],data['fixed_price'])
            cursor.execute(query,args)
            myconn.commit()

        except pymysql.Error as e:
            print("Error lxtrack_cat_producto %d: %s" % (e.args[0], e.args[1]))
            return False

        finally:
            cursor.close()
