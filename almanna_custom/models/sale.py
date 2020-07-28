# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from dateutil.relativedelta import *

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


    def semi_canecl_order(self):
        """
        cancel sale order plus all invoices and payment (reverse )related to order
        """
        #TODO:PDC Cheques must be cancelled also with payment if payment type is cheque
        for rec in self:
            for invoice in rec.invoice_ids:
                for payment in invoice.payment_ids:
                    if payment.state == 'posted':
                        # payment.move_line_ids[0].move_id.state = 'draft'
                        payment.move_line_ids[0].move_id.reverse_moves(date =  payment.move_line_ids[0].move_id.date , journal_id =payment.move_line_ids[0].move_id.journal_id )
                        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>|| ",payment.move_line_ids[0].move_id)
                        # payment.state = 'cancelled'
                        payment.state = 'cancel'
                if invoice.move_id:
                    # invoice.move_id.state = 'draft'
                    invoice.move_id.reverse_moves(date =  invoice.move_id.date , journal_id =invoice.move_id.journal_id )
                    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>|| ",invoice.move_id)
                invoice.state = 'cancel'
                
            rec.state = 'cancel'


    def canecl_order(self):
        """
        cancel sale order plus all invoices and payment related to order
        """
        #TODO:PDC Cheques must be cancelled also with payment if payment type is cheque
        for rec in self:
            for invoice in rec.invoice_ids:
                for payment in invoice.payment_ids:
                    if payment.state == 'posted':
                        # payment.move_line_ids[0].move_id.state = 'draft'
                        payment.move_line_ids[0].move_id.reverse_moves(date =  payment.move_line_ids[0].move_id.date , journal_id =payment.move_line_ids[0].move_id.journal_id )
                        # payment.state = 'cancelled'
                        payment.state = 'cancel'
                if invoice.move_id:
                    # invoice.move_id.state = 'draft'
                    invoice.move_id.reverse_moves(date =  invoice.move_id.date , journal_id =invoice.move_id.journal_id )
                    
                invoice.state = 'cancel'
                
            # rec.state = 'cancel'

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    default_code = fields.Char('Internal Reference',related='product_id.default_code',store=1)

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



class salePlan(models.Model):
    _name = 'sale.plan'

    @api.model
    def default_get(self, fields):
        """ set default value """
        
        result = super(salePlan, self).default_get(fields)
        
        product_obj = self.env['product.product']
        int_references = product_obj.read_group([],['default_code'],['default_code'])
        if result:
            result['name'] = 'Plan-' + str(result['month']) +'-'+str(result['year']) 
            result['line_ids'] = []
            for int_reference in int_references:
                if int_reference['default_code'] != False :
                    result['line_ids'] += [(0, 6, {
                                                    'default_code': int_reference['default_code'],
                                                    'plan_qty': 0,
                                                    'year': result['year'],
                                                    'month': result['month'],
                                                    'total_sale_qty': 0,
                                                    'percentage_done':0,
                                                    
                                                    }),
                                            ] 
        return result

    name = fields.Char(required=1)
    month = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),
    ('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),
    ],required=1,default=str(datetime.now().month))
    #TODO:Must be calculated using range
    year = fields.Selection([
    ('2020','2020'),
    ('2021','2021'),
    ('2022','2022'),
    ('2023','2023'),
    ('2024','2024'),
    ('2025','2025'),],required=1,default=str(datetime.now().year),)
    #TODO:fix value remove error when using auto range ,  
    # year = fields.Selection([(num, str(num)) for num in range((datetime.now().year+5), datetime.now().year-1, -1)],
    #                         string="Year", default=datetime.now().year, required=True)
    # month = fields.Selection([(num, str(num)) for num in range(1, 12 + 1)], string="Month",
    #                           default=datetime.now().month, required=True)
    line_ids = fields.One2many('sale.plan.line','sale_plan_id')

    @api.onchange('month','year')
    def _onchange_date_to_line(self):
        for rec in self.line_ids:
            rec.month = self.month
            rec.year = self.year
        self.line_ids._get_plan_info()

    _sql_constraints = [
        ('uniq_name', 'unique(name)', _("Plan Name must be unique.")),
        ('uniq_date', 'unique(month,year)', _("Plan Date(Month,Year) must be unique.")),
    ]

class salePlanLine(models.Model):
    _name = 'sale.plan.line'


    default_code = fields.Char('Internal Reference(SKU)',required=1)
    plan_qty = fields.Integer('Plan QTY',required=1)
    month = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),
    ('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),
    ],required=1)
    #TODO:Must be calculated 
    year = fields.Selection([
    ('2020','2020'),
    ('2021','2021'),
    ('2022','2022'),
    ('2023','2023'),
    ('2024','2024'),
    ('2025','2025'),],required=1)

    # year = fields.Selection([(num, str(num)) for num in range((datetime.now().year+5), datetime.now().year-1, -1)],
    #                         string="Year", default=datetime.now().year, required=True)
    # month = fields.Selection([(num, str(num)) for num in range(1, 12 + 1)], string="Month",
    #                           default=datetime.now().month, required=True)
    sale_plan_id = fields.Many2one('sale.plan')
    total_sale_qty = fields.Integer(compute='_get_plan_info',readonly=1)
    percentage_done = fields.Float('Done(%)',readonly=1)

    @api.depends('default_code','plan_qty')
    def _get_plan_info(self):
        order_line_obj = self.env['sale.order.line']
        for rec in self:
            if rec.plan_qty:
                total_sale_qty = 0
                # rec.total_sale_qty = total_sale_qty
                month = int(rec.month)
                year = int(rec.year)
                from_date = datetime.strftime(datetime.now().replace(month=month, year=year), "%Y-%m-01")
                to_date = str(datetime.now().replace(month=month, year=year) + relativedelta(months=+1, day=1, days=-1))[:10]
                
                data = order_line_obj.read_group(
                    [
                    ('order_id.confirmation_date','>=',from_date),
                    ('order_id.confirmation_date','<=',to_date) ,
                    ('order_id.state', 'in', ['sale']),
                    ('product_id.default_code', '=', rec.default_code)
                    ],
                    
                    ['product_uom_qty','ss'], ['ss']
                    )
                
                # [
                #     {'__domain': ['&', ('default_code', '=', 'Alwaha 225g'), ('order_id.confirmation_date', '>=', '2020-07-01'), ('order_id.confirmation_date', '<=', '2020-07-31'), ('order_id.state', 'in', ['sale']), ('default_code', '=', 'Alwaha 225g')]
                #     , 'default_code_count': 14,
                #      'default_code': 'Alwaha 225g', 'product_uom_qty': 38.0}
                #      ]

                
                rec.total_sale_qty = data[0]['product_uom_qty'] if len(data) > 0 else 0
                if rec.total_sale_qty:
                    rec.percentage_done =  (rec.plan_qty / rec.total_sale_qty) * 100
                


