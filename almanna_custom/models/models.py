# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class productProduct(models.Model):

    _inherit='product.product'

    #TODO:Fix in Prod DB
    cost_currency_id = fields.Many2one('res.currency',readonly=1)
    

class productTemplate(models.Model):

    _inherit='product.template'

    #TODO:Fix in Prod DB
    cost_currency_id = fields.Many2one('res.currency',readonly=1)




class currency(models.Model):
    _inherit = "res.currency"

    rate = fields.Float(compute='_compute_current_rate', string='Current Rate' #, digits=(12, 6)
    , digits=dp.get_precision('Rate'),
                        help='The rate of the currency to the currency of rate 1.')
    # rounding = fields.Float(string='Rounding Factor' ,# digits=(12, 6),
    #  digits=dp.get_precision('Rate'),
    #  default=0.01)

class currencyRate(models.Model):
    _inherit = "res.currency.rate"


    rate = fields.Float(
        # digits=(12, 6),
    digits=dp.get_precision('Rate')
    , help='The rate of the currency to the currency of rate 1')



class accountMoveLine(models.Model):
    _inherit = "account.move.line"

    debit = fields.Monetary(default=0.0, currency_field='company_currency_id', digits=dp.get_precision('Rate'))
    credit = fields.Monetary(default=0.0, currency_field='company_currency_id', digits=dp.get_precision('Rate'))