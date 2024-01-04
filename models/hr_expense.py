from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class HrExpense(models.Model):
  _inherit = 'hr.expense'
  _description = 'HrExpense'

  report_id = fields.Many2one(
    'hr.expense',
    string='Expense Report', 
    readonly=True, 
    copy=False, domain=[
      ('state', 'in', ['draft', 'reported'])
    ]
  )

  petty_cash_management_id = fields.Many2one(
    'petty.cash.management', 
    string='Petty Cash Management', 
    required='True'
  )

  @api.constrains('petty_cash_management_id')
  def _ckeck_petty_cash_id(self):
    for expense in self:
      if expense.report_id and expense.report_id.petty_cash_management_id \
        != expense.petty_cash_management_id:
          raise ValidationError("You can´t select more than two petty cashes")


  def action_review_expenses(self):
    context_vals = self._get_default_expense_sheet_values()
    if len(context_vals) > 1:
      return {
        'name': _('New Expense Reports'),
        'type': 'ir.actions.act_window',
        'views': [[False, "list"], [False, "form"]],
        'res_model': 'hr.expense.sheet',
        'domain': [('id', 'in', self.petty_cash_management_sheet_id.mapped('id'))],
      }
    else:
      context_vals_def = {}
      for key in context_vals[0]:
        context_vals_def['default_' + key] = context_vals[0][key]
      return {
        'name': _('New Expense Report'),
        'type': 'ir.actions.act_window',
        'views': [[False, "form"]],
        'res_model': 'hr.expense.sheet',
      }