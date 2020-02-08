
from odoo import api, fields, models, _
import time
import pdb
import datetime
from odoo.exceptions import UserError
import logging
from odoo.http import request
_logger = logging.getLogger(__name__)


class RepackWizard(models.TransientModel):
	_name ="repack.package.wizard"
	_description= "Repack Package Wizard"
	_inherit = "stock.quant.package"

	package_ids = fields.Many2many('stock.quant.package', string='Child Package')
	keterangan = fields.Text(string='Keterangan')


	@api.multi
	def move(self):
		active_ids = self._context.get('active_ids')
		active_ids = active_ids or False
		lab_req_obj = self.env['stock.quant.package'].search([])
		lab_reqs = lab_req_obj.browse(active_ids)
		for lab_req in lab_reqs:
			if lab_req.active == False:
				raise Warning('Repack Sudah Menjadi Archive !!')

			lab_reqs.create({
				'name' : "R-"+lab_reqs.name,
				'keterangan' : self.keterangan,
				'package_ids' : [(6,0, self.package_ids.ids)]
				})

			if lab_req.package_ids.name is False:
				lab_req.active = False
			else :
				lab_reqs.active = True