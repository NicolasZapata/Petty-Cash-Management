from odoo import fields, models, api


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    _description = 'Description'

    petty_cash_management_sheet_id = fields.Many2one('petty.cash.management', string='Petty Cash Management', required='True')
