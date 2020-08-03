# -*- coding: utf-8 -*-
from odoo import fields, api, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SalesPlanReport(models.TransientModel):
    _name = 'sales.plan.report.wizard'
    START = datetime.today() - relativedelta(years=10)
    END = datetime.today() + relativedelta(years=10)
    YEARS = [(str(i), str(i)) for i in range(START, END)]
    month = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                              ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'),
                              ], "Month", required=1, default=str(datetime.now().month))
    year = fields.Selection(YEARS, "Year")

    @api.multi
    def print_report(self):
        data = {'month': self.month, 'year': self.year}
        return self.env.ref('sales_plan_report.sales_plan_report').report_action(self, data=data)
