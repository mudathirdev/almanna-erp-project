from odoo import fields , models,api,tools,_
from datetime import datetime,timedelta
from odoo.exceptions import ValidationError
# from odoo import amount_to_text


class FinanceApprovalRequest(models.Model):
    _name = 'custody.request'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Custody Request'

    # def default_employee(self):
    #     return self.env.user.name
    custody_clear_id = fields.Many2one('custody.clear.request',string='Reconcile')

    def default_currency(self):
        return self.env.user.company_id.currency_id

    @api.depends('amount','currency_id')
    def _onchange_amount(self):
        self.num2wo =self.env.user.company_id.currency_id.amount_to_text(self.amount)

    def default_company(self):
        return self.env.user.company_id

    def default_user_analytic(self):
        return self.env.user

    @api.returns('self')
    def _default_employee_get(self):
        return self.env.user

    # def manager_default(self):
    #     return self.env.user.manager_id

    name = fields.Char('Reference',readonly=True,default='New')
    description = fields.Text('Request Description',)
    user_name = fields.Many2one('res.users', string='Employee Name',readonly=False, default=_default_employee_get)

    custody_date = fields.Date('Custody Date', default=lambda self: fields.Date.today(),track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency',default=default_currency,required=True)
    amount = fields.Monetary('Custody Amount',required=True,track_visibility='onchange')
    sequence = fields.Integer(required=True, default=1,)
    state = fields.Selection([('draft','Draft'),
                              ('dm','Submitted'),
                              ('am','Confirmed'),
                              ('fm','Approved'),
                              ('post','Posted'),
                              ('cancel','Cancel')],default='draft', track_visibility='onchange')
    num2wo = fields.Char('Amount In Text',compute='_onchange_amount',store=True)
    company_id = fields.Many2one('res.company',string="Company Name",default=default_company)

    # Accounting Fields
    move_id = fields.Many2one('account.move',string='Move Reference',readonly=True)
    journal_id = fields.Many2one('account.journal',string='Journal / Pay By',domain="[('type','in',['cash','bank'])]")
    custody_journal_id = fields.Many2one('account.journal',string='Custody journal',domain="[('type','=','general')]")
    journal_type = fields.Selection(related='journal_id.type')
    account_id = fields.Many2one('account.account',string='Employee Account',compute='_account_compute')
    user_id = fields.Many2one('res.users', default=default_user_analytic)
    count_journal_entry = fields.Integer(compute='_compute_je')

    @api.one
    def _compute_je(self):
        if self.move_id:
            self.count_journal_entry = 1
        else:
            self.count_journal_entry = 0

    def action_journal_entry(self):

        tree_view = self.env.ref('account.view_move_tree')
        form_view = self.env.ref('account.view_move_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'View Journal Entry',
            'res_model': 'account.move',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'domain': [('id', '=', self.move_id.id)],

        }

    @api.depends('user_name')
    def _account_compute(self):
        # partner_search = self.env['res.partner'].search([('name','=',self.user_name.id),('company_id','=',self.company_id.id)],limit=1)
        self.account_id = self.user_name.pettycash_account_id.id

    analytic_account = fields.Many2one('account.analytic.account',string='Analytic Account')

    def confirm_dm(self):
        if self.amount <= 0:
            raise ValidationError("Please Make Sure Amount Field Grater Than Zero !!")
        if self.env.user.name != self.user_id.name:
            raise ValidationError("Please This Request is not For You")

        self.write({'state': 'dm'})

    def confirm_am(self):

        self.write({'state': 'am'})

    def confirm_fm(self):

        self.write({'state': 'fm'})

        if not self.journal_id or not self.account_id or not self.custody_journal_id:
            raise ValidationError("Please Fill Accounting information (Journal-Employee-Account)")

    @api.model
    def get_amount(self):
        if self.currency_id != self.env.user.company_id.currency_id:
            return self.amount / self.currency_id.rate
        if self.currency_id == self.env.user.company_id.currency_id:
            return self.amount

    @api.model
    def get_currency(self):
        if self.currency_id != self.env.user.company_id.currency_id:
            return self.currency_id.id

    @api.model
    def amount_currency_debit(self):
        if self.currency_id != self.env.user.company_id.currency_id:
            return self.amount

    @api.model
    def amount_currency_credit(self):
        if self.currency_id != self.env.user.company_id.currency_id:
            return self.amount * -1

    # confirm Finance Approval (Posted)
    def confirm_post(self):
        account_move_object = self.env['account.move']
        if not self.account_id or not self.journal_id or not self.custody_journal_id:
            raise ValidationError("Please Make Sure Partner Accounting Tab was Entered or Journal !!")
        if self.account_id and self.journal_id and self.custody_journal_id:
            l = []
            if not self.account_id or not self.journal_id and not self.custody_journal_id:
                raise ValidationError("Please Fill Accounting Information !!")
            # if self.check_term != 'followup':
            debit_val = {
                'move_id': self.move_id.id,
                'name': self.name,
                'account_id': self.account_id.id,
                'debit': self.get_amount(),
                'analytic_account_id': self.analytic_account.id or False,
                'currency_id': self.get_currency() or False,
                'partner_id': self.user_name.partner_id.id,
                'amount_currency': self.amount_currency_debit() or False,
                # 'company_id': self.company_id.id,

            }
            l.append((0, 0, debit_val))
            credit_val = {

                'move_id': self.move_id.id,
                'name': self.name,
                'account_id': self.journal_id.default_credit_account_id.id,
                'credit': self.get_amount(),
                'currency_id': self.get_currency() or False,
                'partner_id': self.user_name.partner_id.id,
                'amount_currency': self.amount_currency_credit() or False,
                # 'analytic_account_id': ,
                # 'company_id': ,

            }
            l.append((0, 0, credit_val))
            print("List", l)
            vals = {
                'journal_id': self.custody_journal_id.id,
                'date': datetime.today(),
                'ref': self.name,
                # 'company_id': ,
                'line_ids': l,
            }
            self.move_id = account_move_object.create(vals)
            self.move_id.post()
            self.state = 'post'

    @api.model
    def create(self, vals):
        code = 'custody.request.code'
        if vals.get('name', 'New') == 'New':
            message = 'PC' + self.env['ir.sequence'].\
            with_context(ir_sequence_date=self.custody_date).next_by_code(code)
            vals['name'] = message
            self.message_post(subject='Create CR', body='This is New CR Number' + str(message))
        return super(FinanceApprovalRequest, self).create(vals)

    @api.multi
    def unlink(self):
        for i in self:
            if i.state != 'draft':
                raise ValidationError("Please Make Sure State in DRAFT !!")
            else:
                super(FinanceApprovalRequest, i).unlink()

    def copy(self):
        raise ValidationError("Can not Duplicate a Record !!")

    def cancel_request(self):

        if self.custody_journal_id.update_posted == False:
            raise ValidationError("Please Check Allow Cancel Journal Entry In Journal First !!")
        else:
            # Cancel JE and Delete it
            self.move_id.button_cancel()
            self.move_id.unlink()
            self.state = 'cancel'

    def reject(self):
        self.state = 'draft'


class Inheritrespartner(models.Model):
    _inherit = 'res.partner'

    pettycash_account_id = fields.Many2one('account.account',string='Custody account')