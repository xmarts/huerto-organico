# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp

from odoo.tools import pycompat
from odoo.tools.translate import html_translate
from odoo.tools import float_is_zero


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    parent_website_id = fields.Many2one('product.public.category')
    dependecy_website_ids = fields.One2many('product.public.category', 'parent_website_id')

