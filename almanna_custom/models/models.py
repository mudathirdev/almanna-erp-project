# -*- coding: utf-8 -*-

from odoo import models, fields, api


class saleOrder(models.Model):

    _inherit='sale.order'

    location_id = fields.Many2one('stock.location')

    def canecl_order(self):
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

# class stockMove(models.Model):

#     _inherit='stock.move'

#     @api.model
#     def create(self,vals):

#         stock_picking_data = self.env['stock.picking.type'].browse(vals.get('picking_type_id'))
#         # if self.sale_id:
#         #     self.location_id = self.sale_id.location_id
#         # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.HERERE",stock_picking_data)
#         # if stock_picking_data.code == 'incoming':

#         #     warehouse_data = self.env['stock.warehouse'].browse(vals.get('warehouse_id'))

#         #     if warehouse_data:
#         #         print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",warehouse_data)
                

#         #         #your condition here which location you want to set.

#         return super(stockMove,self).create(vals)




                
#         # if vals.get('sale_id',False):
#         #     sale_order = self.env['sale.order'].search([('id','=',vals.get('sale_id'))])
#         #     vals['location_id'] = sale_order.location_id