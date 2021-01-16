# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    max_distance_to_sell = fields.Integer(
        string='Max Distance to Sell',
        default=0.0,
        help='Define maximum distance to allow sale in meters.',)
