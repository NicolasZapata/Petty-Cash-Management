from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class HrExpense(models.Model):
  _inherit = 'hr.expense'
  _description = 'HrExpense'
  
  petty_cash_management_id = fields.Many2one('petty.cash.management', string='Petty Cash Management', required='True')
  