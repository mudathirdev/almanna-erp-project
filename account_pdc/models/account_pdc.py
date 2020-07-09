# -*- coding: utf-8 -*-

from odoo import models, fields, api,tools, _
from odoo.exceptions import UserError, except_orm

class AccountPDC(models.Model):
    _name = 'account.pdc'
    _inherit = ['mail.thread']
    _description = "PDC"
    _order = 'maturity_date desc'

    name = fields.Char('Reference')
    type = fields.Selection([('customer','Customer'),('vendor','Vendor')])
    maturity_date = fields.Date('Maturity Date')
    partner_id = fields.Many2one('res.partner', 'Partner')
    journal_id = fields.Many2one('account.journal', 'Clearing Journal', domain=[('type', 'in', ('bank', 'cash')), ('is_check_journal','!=', True)])
    payment_id = fields.Many2one('account.payment', 'Payment')
    state = fields.Selection([('draft','New'),('reject','Rejected'),('clear','Cleared')], default='draft', track_visibility="onchange")
    amount = fields.Monetary()
    currency_id = fields.Many2one('res.currency', "Currency")
    move_id = fields.Many2one('account.move', "Journal Entry")
    company_id = fields.Many2one('res.company', "Company", default=lambda self: self.env.user.company_id)
    note = fields.Text()


    @api.one
    def clear(self):
        AccountMove = self.env['account.move']
        AccountMoveLine = self.env['account.move.line'].with_context(check_move_validity=False)
        if not self.journal_id:
            raise UserError('Select Clearing Journal')
        Move = AccountMove.create({
            'journal_id': self.journal_id.id,
            'ref': 'Check Clearing: ' + self.name
        })
        debit_line = {}
        credit_line = {}
        if self.type == 'customer':
            debit_line['account_id'] = self.journal_id.default_debit_account_id.id
            credit_line['account_id'] = self.payment_id.journal_id.default_credit_account_id.id
        else:
            credit_line['account_id'] = self.journal_id.default_credit_account_id.id
            debit_line['account_id'] = self.payment_id.journal_id.default_debit_account_id.id

        debit_line['partner_id'] = self.partner_id.id
        debit_line['name'] = 'Check Clearing: ' + self.name
        debit_line['debit'] = self.amount
        debit_line['credit'] = 0.0
        debit_line['move_id'] = Move.id

        credit_line['partner_id'] = self.partner_id.id
        credit_line['name'] = 'Check Clearing: ' + self.name
        credit_line['debit'] = 0.0
        credit_line['credit'] = self.amount
        credit_line['move_id'] = Move.id

        AccountMoveLine.create(debit_line)
        AccountMoveLine.create(credit_line)
        Move.post()
        self.state = 'clear'
        self.move_id = Move.id

    # fields.Date.today()
    @api.one
    def reject(self):
        partner_account = False
        if self.type == 'customer':
            partner_account =  self.payment_id.partner_id.property_account_receivable_id
        else:
            partner_account =  self.payment_id.partner_id.property_account_payable_id

        for move in self.payment_id.move_line_ids.mapped('move_id'):
            move.reverse_moves(fields.Date.today(), move.journal_id or False)
            move.line_ids.remove_move_reconcile()
            self.payment_id.move_line_ids.filtered(lambda r: r.account_id == partner_account).reconcile()

        self.payment_id.state = 'cancel'
        self.state = 'reject'


    @api.one
    def soft_reject(self):
        self.move_id.state = 'draft'
        self.state = 'reject'