# -*- coding: utf-8 -*-
from odoo.addons.website_sale_options.controllers.main import WebsiteSale as WebsiteSale_options
from odoo.http import request
from odoo import http

class WebsiteSale(WebsiteSale_options):

    def _get_search_domain(self, search, category, attrib_values):
        domain = super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)

        order = request.website.sale_get_order()
        if not order:
            domain += [('public_categ_ids.dependecy_website_ids.id', '=', False)]
        else:
            domain += [ '|','|',
                ('public_categ_ids.dependecy_website_ids.id', 'in', order.mapped('order_line.product_id.public_categ_ids').ids),
                ('public_categ_ids.dependecy_website_ids', '=', False),
                ('public_categ_ids', '=', False)
            ]
        return domain

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=False):
        result = super(WebsiteSale, self).cart_update_json(product_id, line_id, add_qty, set_qty, display)
        order = request.website.sale_get_order()
        result['cart_quantity'] = order.cart_quantity
        from_currency = order.company_id.currency_id
        to_currency = order.pricelist_id.currency_id

        result['website_sale.cart_lines'] = request.env['ir.ui.view'].render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'compute_currency': lambda price: from_currency.compute(price, to_currency),
            'suggested_products': order._cart_accessories()
        })

        return result

