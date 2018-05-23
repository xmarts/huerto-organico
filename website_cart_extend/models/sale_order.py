# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, models, fields, _
from odoo.http import request
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None, **kwargs):
        result = super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, attributes=attributes, **kwargs)

        public_categ_ids = self.mapped('order_line.product_id.public_categ_ids').ids

        update_line = self.order_line.filtered(lambda x: \
                                        x.product_id.public_categ_ids and \
                                        x.product_id.public_categ_ids.dependecy_website_ids and \
                                        x.product_id.public_categ_ids.dependecy_website_ids.id not in public_categ_ids)

        public_categ_ids = update_line.mapped('product_id.public_categ_ids.dependecy_website_ids.id')
        update_line.unlink()
        result['public_categ_ids'] = public_categ_ids
        return result

