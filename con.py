import xmlrpc.client
import pymysql



from pprint import pprint

#conexion odoo
url = 'https://xmarts-embotelladora-el-jarocho-19-06-450101.dev.odoo.com'
db = 'xmarts-embotelladora-el-jarocho-19-06-450101'
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

class ProductPricelist():
    def read(self):
        # Read ProductsPricelist
        model_name = 'product.pricelist'
        partner_ids = models.execute_kw(db, uid, password, 'product.pricelist', 'search',
                                        [[['rental', '=', False]]])  # ,{'limit': 10})
        #ids = models.execute_kw(db, uid, password, 'product.template', 'search',
        #                                [[['rental', '=', False]]]) #,{'limit': 10})
        #records = models.execute_kw(db, uid, password, model_name, 'read', [ids])
        #return records

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
        model_name = 'lx_price'
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

        #    if cursor.lastrowid:
        #        print('last insert id', cursor.lastrowid)
        #    else:
        #        print('last insert id not found')
            myconn.commit()


        except pymysql.Error as e:
            print("Error lxtrack_cat_producto %d: %s" % (e.args[0], e.args[1]))
            return False

        finally:
            cursor.close()

