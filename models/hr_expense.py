from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrExpense(models.Model):
    _inherit = "hr.expense"
    _description = "HrExpense"

    petty_cash_management_id = fields.Many2one(
        "petty.cash.management", string="Petty Cash Management", required="True"
    )

    # TODO: Ajust for filter two petty cashes and get an validation error
    @api.constrains("petty_cash_management_id")
    def action_ckeck_petty_cash_id(self):
        for expense in self:
            if (
                expense
                and expense.report_id.petty_cash_management_id
                != expense.petty_cash_management_id
            ):
                raise ValidationError(
                    "You cant select more than two petty cashes"
                )
