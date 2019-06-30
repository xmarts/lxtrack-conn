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

class RouteOrder():
    def read(self,status):
        # read route.order
        model_name = 'route.order'
        ids = models.execute_kw(db, uid, password, model_name , 'search',
                                        [[['state', '=', 0]]])  # ,{'limit': 10})
        records = models.execute_kw(db, uid, password, model_name, 'read', [ids])
        return records

class Partners():
    def read(self,id):
        # Read customers
        model_name = 'res.partner'
        partner_ids = models.execute_kw(db, uid, password, model_name, 'search',
                                        [[['id', '=', id]]]) #,{'limit': 10})
        partner_records = models.execute_kw(db, uid, password, model_name, 'read', [partner_ids])
        return partner_records



#Clases para mysql

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


class lxtrack_cliente():
    def insert(self,data):
        cursor = myconn.cursor()
        try:
            query = "INSERT INTO lxtrack_cliente " \
                    "(id, id_local, razon_social, nombre_comercial, RFC, askticket, credito, limite_credito, detallesaldo, montodebe, codigo_cliente,"\
                    "id_lista_precios, id_categoria_sector, autorizado, capture, active, id_inactive_reason, insert_date, mod_date, id_usuario_creator, id_usuario_last_editor, id_sesion_app) "\
                    "VALUES(%s, %s, %s, %s, %s, '0', %s, %s, NULL, 0, %s " \
                    ", 1, 1, '1', 'P', '1', NULL, '2018-05-11 13:56:13.000', '2018-07-04 14:47:22.000', 0, 0, NULL) " \
                    " ON DUPLICATE KEY UPDATE razon_social  = %s, nombre_comercial = %s, RFC = %s, credito = %s, limite_credito = %s "
            args = (data['id'],data['id'],data['name'],data['name'],data['vat'],data['credit'],data['credit_limit'],data['id'],
                    data['name'],data['name'],data['vat'],data['credit'],data['credit_limit'])
            cursor.execute(query,args)
            myconn.commit()

        except pymysql.Error as e:
            print("Error lxtrack_cat_producto %d: %s" % (e.args[0], e.args[1]))
            return False

        finally:
            cursor.close()



class lxtrack_cliente_direccion():
    def insert(self,data,cliente):
        cursor = myconn.cursor()
        try:
            query = "INSERT INTO LX_JAROCHITO.lxtrack_cliente_direccion "\
                    "(id, id_cliente, clave_estado, ciudad, colonia, domicilio, "\
                    "cp, lat, lon, radio, nombre, contacto, tel, email, tipo, ruta, id_cluster, active, id_inactive_reason, insert_date, mod_date, id_usuario_creator, id_usuario_last_editor) "\
                    " VALUES(%s, %s, %s, %s, %s, %s, "\
                    " %s, %s, %s, 50, %s, 'cliente', %s, %s, 'M', 0, NULL, '1', NULL, %s, %s, 0, 0) " \
                    " ON DUPLICATE KEY UPDATE id_cliente = %s, clave_estado = %s, ciudad = %s, colonia = %s , domicilio = %s " \
                    ", cp = %s , lat = %s , lon = %s , nombre = %s , contacto = %s "# , tel = %s , email = %s , mod_date = %s ) "
            args = (data['id'],data['id'],data['state_id'][1],data['l10n_mx_edi_locality'],data['l10n_mx_edi_colony'],data['street_name']+' '+str(data['street_number']),
                    str(data['zip']),data['partner_latitude'],data['partner_longitude'],data['name'],data['phone'],data['email'],data['create_date'],data['__last_update'],
                    data['id'],data['state_id'][1],data['l10n_mx_edi_locality'],data['l10n_mx_edi_colony'],data['street_name']+' '+str(data['street_number'])
                    ,str(data['zip']) ,data['partner_latitude'],data['partner_longitude'] ,data['name'] ,data['name'] , data['phone'] )#,data['email'],data['__last_update'])
            cursor.execute(query,args)
            myconn.commit()

        except pymysql.Error as e:
            print("Error lxtrack error  %d: %s" % (e.args[0], e.args[1]))
            return False

        finally:
            cursor.close()
