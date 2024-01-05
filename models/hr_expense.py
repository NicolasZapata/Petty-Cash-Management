from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class HrExpense(models.Model):
  _inherit = 'hr.expense'
  _description = 'HrExpense'

  petty_cash_management_id = fields.Many2one(
    'petty.cash.management', 
    string='Petty Cash Management', 
    required='True'
  )

  @api.constrains('petty_cash_management_id')
  def _ckeck_petty_cash_id(self):
    for expense in self:
      if expense.report_id and expense.petty_cash_management_id.expense_ids.filtered(lambda x: x.id != expense.id):
          raise ValidationError("You can´t select more than two petty cashes")
