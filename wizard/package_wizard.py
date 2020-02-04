
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

	package_ids = fields.One2many('stock.quant.package', 'package_baru_id', string='Child Package')
	keterangan = fields.Text(string='Keterangan')


	@api.multi
	def move(self):
		obj_package = self.env['stock.quant.package'].create({
			'name' : "R-"+self.name,
			'package_ids' : self.package_ids,
		})