# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    @api.model
    def default_get(self, fields):
        """ set default value for location based on selected warehouse """
        
        result = super(SaleOrder, self).default_get(fields)
        if 'warehouse_id' in result:
            warehouse_obj = self.env['stock.warehouse']
            result['location_id'] = warehouse_obj.browse(result['warehouse_id']).lot_stock_id.id
        return result


    location_id = fields.Many2one('stock.location', 'Location', domain="[('usage', '=', 'internal')]",)
    


    @api.onchange('warehouse_id')
    def _onchange_warehouse_location_domain(self):
        """in case wharehouse change then we need to change location to default location of new selected wharehouse 
           also set domain for child of new selected whrehouse
        """
        
        location_obj = self.env['stock.location']
        location_id = self.warehouse_id.lot_stock_id # main warehouse location
        location_parent = location_id.location_id #location id is parent location n model stock.location
        
        
        self.location_id = location_id
        child_locations = location_obj.search([('id','child_of',location_parent.id),('usage', '=', 'internal')])
        
        
        return {'domain': {'location_id': [('id','in',child_locations.ids),('usage', '=', 'internal')]}}


    def canecl_order(self):
        """
        cancel sale order plus all invoices and payment related to order
        """
        #TODO:PDC Cheques must be cancelled also with payment if payment type is cheque
        for rec in self:
            for invoice in rec.invoice_ids:
                for payment in invoice.payment_ids:
                    if payment.state == 'posted':
                        payment.move_line_ids[0].move_id.state = 'draft'
                         
                        # payment.state = 'cancelled'
                        payment.state = 'cancel'
                if invoice.move_id:
                    invoice.move_id.state = 'draft'
                invoice.state = 'cancel'
            rec.state = 'cancel'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _action_launch_procurement_rule(self):
        """
        change Source location to selected location in the sale order and state start from draft
        """
        res = super(SaleOrderLine, self)._action_launch_procurement_rule()
        for rec in self:
            #why sudo()?!!!
            deliveries = rec.env['stock.picking'].sudo().search([('sale_id', '=', rec.order_id.id)])
            for delivery in deliveries:
                values = {
                        'state': 'draft'
                    }
                if rec.order_id.location_id:
                    values.update(location_id = rec.order_id.location_id.id)
                delivery.sudo().write(values)
        return res
