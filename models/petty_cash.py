from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError


class PettyCashManagement(models.Model):
      _name = 'petty.cash.management'
      _description = 'PettyCash'
      
      responsable_id = fields.Many2one('hr.employee', string='responsable')
      cash_amount = fields.Float(string='cash_amount')
      cash_notes = fields.Html(string='cash_notes')
      date_closed = fields.Date(string='date_closed')
      date_opened = fields.Date(string='date opened')
      refund_account_id = fields.Many2one('account.account', string='refund_account')
      expense_to_report = fields.Float(string='Expense to report')
      validation_expenses = fields.Float(string='Validation Expenses')
      expenses_to_reimburse = fields.Float(string='Expenses to reimburse')
      cash_on_hand = fields.Float(string='Cash on hand')
      total = fields.Float(string='total', compute="total_cash_amount", store=True)

      @api.depends('expense_to_report', 'validation_expenses')
      def total_cash_amount(self):
            self.total = self.expense_to_report + self.validation_expenses