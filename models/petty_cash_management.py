from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError


class PettyCashManagement(models.Model):
    _name = 'petty.cash.management'
    _description = 'PettyCash'
    
    responsable_id = fields.Many2one('hr.employee', string='responsable')
    cash_amount = fields.Float('cash_amount')
    cash_notes = fields.Text('cash_notes')
    date_opened = fields.Date('date_opened')
    date_closed = fields.Date('date_closed')
    refund_account_id = fields.Many2one('account.account', string='refund_account')
