from psycopg2 import OperationalError, Error

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_is_zero

import logging


class QtyProduction(models.Model):
    _name = 'qty.product'
    _rec_name ='partner_id'
    

    partner_id = fields.Many2one(
        string='Customer',
        comodel_name='res.partner', required=True
    )
    
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product', required=True
    )
    
    
    qty_kecil = fields.Float(string='Qty Kecil', required=True)
    qty_besar = fields.Float(string='Qty Besar', required=True)

    _sql_constraints = [
        ('cek_unik_name', 'UNIQUE(partner_id,product_id)',
            'Customer dan Product harus unik')
    ]

     