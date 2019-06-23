import xmlrpc.client
from datetime import datetime

# url = "http://localhost:8069"
# db = "RAJO"
# username = 'a'
# password = 'a'
url = "http://localhost:8070"
db = "jarochito"
username = 'admin'
password = 'admin'
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))


class Partners():
    def read(self):
        # Read customers
        model_name = 'res.partner'
        partner_ids = models.execute_kw(db, uid, password, model_name, 'search', [[['customer', '=', True]]])
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


class Product():
    # Read product
    def read(self):
        model_name = 'product.product'
        product = models.execute_kw(db, uid, password, model_name, 'search_read', [[]], {'limit': 1})[0]


class Candidate():
    def read(self):
        # # Read candidate
        model_name = 'rajo.candidate'
        candidate = models.execute_kw(db, uid, password, model_name, 'search_read', [[]], {'limit': 1})[0]


class SaleOrder():
    def read(self):
        # Read sale order
        model_name = 'sale.order'
        order_ids = models.execute_kw(db, uid, password, model_name, 'search', [[]])
        order_records = models.execute_kw(db, uid, password, model_name, 'read', [order_ids])

    def create(self, partner_id, candidate_id, line_name, product_id):
        # Create sale order
        model_name = 'sale.order'
        vals = {
            'origin': "A555",
            'client_order_ref': "B555",
            'partner_id': partner_id,  # api partner
            'pricelist_id': 1,  # Public Pricelist (KWD)
            'partner_invoice_id': partner_id,
            'partner_shipping_id': partner_id,
            'order_line': [(0, 0, {
                'name': line_name,
                'product_id': product_id,
                'product_uom_qty': 2,
                'qty_delivered': 2,
                'price_unit': 1000.00,
                'candidate_id': candidate_id,
            })]
        }
        new_id = models.execute_kw(db, uid, password, model_name, 'create', [vals])
        return new_id


class Ticket():
    def read(self):
        # Read ticket
        model_name = 'helpdesk.ticket'
        tickets = models.execute_kw(db, uid, password, model_name, 'search_read', [[['partner_id', '=', partner['id']]]])

    def create(self, partner_id, candidate_id):
        # Create ticket
        model_name = 'helpdesk.ticket'
        vals = {
            'name': "Test ticket",
            'partner_id': partner_id,
            'candidate_id': candidate_id,
        }
        new_id = models.execute_kw(db, uid, password, model_name, 'create', [vals])
        return new_id


class Payment():
    def create(self, sale_order_id):
        # Create invoice and register payment
        model_name = 'sale.order'
        models.execute_kw(db, uid, password, model_name, 'action_confirm', [[sale_order_id]])
        new_invoice_id = models.execute_kw(db, uid, password, model_name, 'action_invoice_create', [[sale_order_id]])
        model_name = 'account.invoice'
        models.execute_kw(db, uid, password, model_name, 'action_invoice_open', new_invoice_id)
        ctx = {'active_model': 'account.invoice', 'active_ids': new_invoice_id}
        vals = {
            'payment_date': str(datetime.now()),
            'journal_id': 7,  # Bank journal ID
            'payment_method_id': 1,  # manual
            'amount': 2000.00,
        }
        model_name = 'account.register.payments'
        registered_payment_id = models.execute_kw(db, uid, password, model_name, 'create', [vals], {'context': ctx})
        models.execute_kw(db, uid, password, model_name, 'create_payment', [[registered_payment_id]], {'context': ctx})
