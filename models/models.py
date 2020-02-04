from odoo import models, fields, api, _
from odoo.exceptions import UserError


class stockmovee(models.Model):
    _inherit = 'stock.move'
    
    customer_id = fields.Many2one(
        'qty.product', 'Customer ',
        states={'done': [('readonly', True)]})

    def _get_default_label(self):
        context = self.env.context
        if context.get('active_model') == 'stock.quant':
            return context.get('active_ids', False)
        return False
    
    qty_kecil = fields.Float(string='Std Qty', related="customer_id.qty_kecil")
    qty_kecil_dus = fields.Float(string='Jml Std Qty', compute="_jumlah_dus_kecil")
    qty_besar = fields.Float(string='Std Qty', related="customer_id.qty_besar")
    qty_besar_dus = fields.Float(string='Jml Std Qty', compute="_jumlah_dus_besar")
    qty_non_std = fields.Float(string='Jml Std Qty', compute="_jumlah_non_standar")

    label_besar_ids = fields.Many2many(comodel_name='stock.quant.package', string="Label Besar",
                                        required=False, copy=False)




    @api.depends('product_uom_qty','qty_kecil')
    def _jumlah_dus_kecil (self):
        for x in self:
            if x.qty_kecil > 0:
                x.qty_kecil_dus = x.product_uom_qty // x.qty_kecil
            else :
                x.qty_kecil_dus = 0


    @api.depends('product_uom_qty','qty_besar')
    def _jumlah_dus_besar (self):
        for x in self:
            if x.qty_besar > 0:
                x.qty_besar_dus = x.product_uom_qty // x.qty_besar
            else :
                x.qty_besar_dus = 0
                
    @api.depends('product_uom_qty','qty_besar')
    def _jumlah_non_standar (self):
        for x in self:
            if x.qty_kecil > 0:
                x.qty_non_std = x.product_uom_qty - (x.qty_kecil * x.qty_kecil_dus)
            else :
                x.qty_non_std = 0



    @api.multi
    def action_create_package(self):
        jml_looping_dus_besar = int(self.qty_besar_dus)
        besar = 0
        
        for db in range(jml_looping_dus_besar) :
            besar += 1
            obj_package_besar = self.env['stock.quant.package'].create({
                'name' : self.lot.name+"/B/"+ str(besar)
            })
            

            self.label_besar_ids = [(4,obj_package_besar.id)]
    
        jml_looping_dus_kecil = int(self.qty_kecil_dus)
    
        
        kecil = 0
        if self.move_line_ids :
            kecil += 1
            obj_package = self.env['stock.quant.package'].create({
                'name' : self.lot.name+"/K/"+ str(kecil)
            })
            for x in self.move_line_ids :
                x.qty_done = self.qty_kecil
                x.lot_id = self.lot.id
                x.result_package_id = obj_package.id
                jml_looping_dus_kecil -= 1 
              
       
        
       
        for ml in range(jml_looping_dus_kecil) :
            kecil += 1
            obj_package = self.env['stock.quant.package'].create({
                'name' : self.lot.name+"/K/"+ str(kecil)
            })
            
            self.move_line_ids.create({
                'product_id' : self.product_id.id,
                'product_uom_id' : self.product_id.uom_id.id,
                'qty_done' : self.qty_kecil,
                'product_uom_id' : self.product_id.uom_id.id,
                'location_id' : self.location_id.id,
                'picking_id' : self.picking_id.id,
                'location_dest_id' : self.location_dest_id.id,
                'move_id' : self.id,
                'lot_id' : self.lot.id,
                'result_package_id' : obj_package.id

            })
            
        non_std = kecil
        if self.qty_non_std > 0 :
            non_std += 1
            obj_package_non = self.env['stock.quant.package'].create({
                'name' : self.lot.name+"//K/"+ str(non_std)
            })
            self.move_line_ids.create({
                'product_id' : self.product_id.id,
                'product_uom_id' : self.product_id.uom_id.id,
                'qty_done' : self.qty_non_std,
                'product_uom_id' : self.product_id.uom_id.id,
                'location_id' : self.location_id.id,
                'picking_id' : self.picking_id.id,
                'location_dest_id' : self.location_dest_id.id,
                'move_id' : self.id,
                'lot_id' : self.lot.id,
                'result_package_id' : obj_package_non.id
            })
        
        
        if self.qty_kecil_dus > 0 :
            pembagi = int(self.qty_kecil_dus) / int(self.qty_besar_dus)
        else : 
            pembagi = 0
            
        
        obj_kecil = self.env['stock.quant.package'].search([('name','ilike',self.lot.name+"/K/")],order='id asc')
        
        i = 0
        for bs in self.label_besar_ids :
            data_kecil = []
            
            for j in range(0,int(pembagi)) :
                data_kecil.append((4,obj_kecil[i].id))
                name_kecil = obj_kecil[i].name.split('/')
                obj_kecil[i].name = bs.name+"/" + name_kecil[3]+"/" +name_kecil[4]
                i += 1 
                
               
                
            bs.package_ids = data_kecil
                
        