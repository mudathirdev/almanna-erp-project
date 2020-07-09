# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    location_id = fields.Many2one('stock.location', 'Location', domain="[('usage', '=', 'internal')]")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _action_launch_procurement_rule(self):
        res = super(SaleOrderLine, self)._action_launch_procurement_rule()
        for rec in self:
            deliveries = rec.env['stock.picking'].sudo().search([('sale_id', '=', rec.order_id.id)])
            for delivery in deliveries:
                delivery.sudo().write({
                    'location_id': rec.order_id.location_id.id,
                    'state': 'draft'
                })
        return res
