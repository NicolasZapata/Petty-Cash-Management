from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError

class PettyCashManagement(models.Model):
      _name = 'petty.cash.management'
      _description = 'PettyCash'
      # _inherit = 'hr.expense'

      name = fields.Char(string='Petty Cash Management')
      responsable_id = fields.Many2one('hr.employee', string='responsable')
      cash_amount = fields.Float(string='cash_amount')
      cash_notes = fields.Html(string='cash_notes')
      date_closed = fields.Date(string='date_closed')
      date_opened = fields.Date(string='date opened')
      refund_account_id = fields.Many2one('account.account', string='refund_account')
      expense_ids = fields.One2many('hr.expense','petty_cash_management_id', string='Expenses')
      expense_to_report = fields.Float(string='Expense to Report', compute='_compute_expense_to_report', readonly='True', store='True')
      expenses_to_approve = fields.Float(string='Expenses to validate', compute='_compute_expenses_to_approve', readonly='True', store='True')
      expenses_to_reimburse = fields.Float(string='Expenses to reimburse', compute='_compute_expense_to_reimburse', readonly='True', store='True')
      cash_on_hand = fields.Float(compute="_total_cash_amount", string='Cash on hand')

      expense_to_draft = fields.Float(string='Expense to Draft', compute='_compute_expense_to_draft', readonly='True', store='True')
      expenses_to_approve = fields.Float(string='Expense to Approve', compute='_compute_expenses_to_approve', readonly='True', store='True')

      petty_cash_states = fields.Selection([
            ('draft', 'draft'),
            ('open', 'open'),
            ('closed', 'closed')
      ], string='Petty Cash States')

      # COMPUTE METHODS
      #Expenses to report state is in draft
      @api.depends('expense_ids', 'expense_ids.state', 'expense_ids.total_amount')
      def _compute_expense_to_report(self):
            for record in self:
                  report_expenses = (record.expense_ids.filtered(lambda expense: expense.state == 'draft'and expense.petty_cash_management_id == record))
                  record.expense_to_report = sum(report_expenses.mapped('total_amount'))

      #Expenses to approve state is in reported
      @api.depends('expense_ids', 'expense_ids.state', 'expense_ids.total_amount')
      def _compute_expenses_to_approve(self):
            for record in self:
                  approve_expenses = (record.expense_ids.filtered(lambda expense: expense.state == 'reported' and expense.petty_cash_management_id == record))
                  record.expenses_to_approve = sum(approve_expenses.mapped('total_amount'))


      #Expenses to reimburse state is in approved
      @api.depends('expense_ids', 'expense_ids.state', 'expense_ids.total_amount')
      def _compute_expense_to_reimburse(self):
            for record in self:
                  reimburse_expenses = (record.expense_ids.filtered(lambda expense: expense.state == 'approved' and expense.petty_cash_management_id == record))
                  record.expenses_to_reimburse = sum(reimburse_expenses.mapped('total_amount'))

      @api.depends('expense_ids', 'expense_ids.state', 'expense_ids.total_amount')
      def _total_cash_amount(self):
            self.cash_on_hand = (self.cash_amount \
                                 - self.expense_to_report \
                                 - self.expenses_to_approve \
                                 - self.expenses_to_reimburse)

