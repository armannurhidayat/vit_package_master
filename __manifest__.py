# -*- coding: utf-8 -*-
{
    'name': "Package Product",

    'summary': """
        Package Product dari MO ke dalam package box besar dan kecil""",

    'description': """
    version 0.1 =  Package Product dari MO ke dalam package box besar dan kecil
    version 0.2 =  fix inherit form stock move
    """,

    
    'author': 'Arman Nur Hidayat',
    'website': 'http://www.vitraining.com',

    
    'category': 'Uncategorized',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','vit_mrp_cost','sale','vit_mrp_lot'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/inherit_stock.xml',
        'views/qty_product.xml',
        'views/package.xml',
        'wizard/package_wizard.xml',
        # 'data/ir_sequence_lot.xml',
        
    ],
  
}