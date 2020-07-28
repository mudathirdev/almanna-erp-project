# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import date,datetime,timedelta
from dateutil.relativedelta import *

class purchaseOrder(models.Model):
    _inherit = 'purchase.order'

    days_passed = fields.Integer(compute="_get_due_info")
    days_left = fields.Integer(compute="_get_due_info")

    def _get_due_info(self):
        for rec in self:
            rec.days_passed = 1
            rec.days_left = 1
            # receiving_days = date.today() - rec.date_order if rec.date_order else 0
            # if receiving_days != 0 and receiving_days.days <= 0:
            #     receiving_days = 0
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>.",date.today() ,rec.date_order)
            # receiving_days = str(receiving_days).replace("0:00:00","").replace(",","")
            # receiving_days_num = int(receiving_days.replace('Days','').replace('days','').replace('day',''))

            # total_sale_qty = 10
            # # rec.total_sale_qty = total_sale_qty
            # month = int(rec.month)
            # year = int(rec.year)
            # from_date = datetime.strftime(datetime.now().replace(month=month, year=year), "%Y-%m-01")
            # to_date = str(datetime.now().replace(month=month, year=year) + relativedelta(months=+1, day=1, days=-1))[:10]
            
            # data = self.env['sale.order.line'].read_group(
            #     [
            #     ('order_id.confirmation_date','>=',from_date),
            #     ('order_id.confirmation_date','<=',to_date) ,
            #     ('order_id.state', 'in', ['sale']),
            #     ('default_code', '=', rec.default_code)
            #     ],
                
            #     ['product_uom_qty','default_code'], ['default_code']
            #     )


            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>||||  ",data[0]['product_uom_qty'] if len(data) > 0 else [])
            
            # rec.total_sale_qty = data[0]['product_uom_qty'] if len(data) > 0 else 0
            # rec.percentage_done =  (rec.total_sale_qty/rec.plan_qty) * 100
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>|||| total_sale_qty ",rec.total_sale_qty)



