from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError


class PettyCashManagement(models.Model):
    _name = "petty.cash.management"
    _description = "PettyCash"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Petty Cash Management")
    responsable_id = fields.Many2one("hr.employee", string="Responsable")
    cash_amount = fields.Float(string="Cash Amount", tracking=True)
    cash_notes = fields.Html(string="Cash Notes", tracking=True)
    date_closed = fields.Date(string="Date Closed", tracking=True)
    date_opened = fields.Date(string="Date Opened", tracking=True)
    refund_account_id = fields.Many2one("account.account", string="Refund Account")
    expenses_count = fields.Integer(
        string="Expenses Count", compute="_compute_expenses_count"
    )
    expense_ids = fields.One2many(
        "hr.expense", "petty_cash_management_id", string="Expenses"
    )
    expense_sheets_ids = fields.One2many(
        "hr.expense.sheet", "petty_cash_management_sheet_id", string="Expenses"
    )
    expense_to_report = fields.Float(
        string="Expense to Report",
        compute="_compute_expense_to_report",
        readonly="True",
        store="True",
    )
    expenses_to_approve = fields.Float(
        string="Expenses to validate",
        compute="_compute_expenses_to_approve",
        readonly="True",
        store="True",
    )
    expenses_to_reimburse = fields.Float(
        string="Expenses to reimburse",
        compute="_compute_expense_to_reimburse",
        readonly="True",
        store="True",
    )
    cash_on_hand = fields.Float(
        compute="_total_cash_amount", string="Cash on hand", tracking=True
    )
    expenses_to_approve = fields.Float(
        string="Expense to Approve",
        compute="_compute_expenses_to_approve",
        readonly="True",
        store="True",
    )
    petty_cash_states = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open Petty Cash"),
            ("closed", "Close Petty Cash"),
        ],
        string="Petty Cash States",
        default="draft",
    )

    # Buttons
    def btnDraftPettyCash(self):
        self.petty_cash_states = "draft"

    def btnOpenPettyCash(self):
        self.petty_cash_states = "open"

    def btnClosePettyCash(self):
        self.petty_cash_states = "closed"

    # Smart Buttons
    def action_open_expenses_view(self):
        """
        Open the expenses view for a single record.
        """
        # Ensure there is only one record
        self.ensure_one()

        # Return the action dictionary
        return {
            "name": _("Expenses"),  # Set the name of the action
            "type": "ir.actions.act_window",  # Set the type of action
            "view_mode": "list,form",  # Set the view modes
            "res_model": "hr.expense",  # Set the model for the action
            "domain": [
                ("id", "in", self.expense_ids.ids)
            ],  # Set the domain filter
        }

    def action_open_expenses_reports(self):
        self.ensure_one()
        return self.env.ref("hr_expense.action_hr_expense_sheet_all").read()[0]

    def action_generate_expense_invoice(self):
        self.ensure_one()
        return self.env.ref("hr_expense.action_report_hr_expense_sheet").read()[0]

    def _compute_expenses_count(self):
        for rec in self:
            expenses_count = self.env["hr.expense"].search_count(
                [("id", "=", rec.expense_ids.ids)]
            )
            rec.expenses_count = expenses_count

    # COMPUTE METHODS
    # Expenses to report state is in draft
    @api.depends("expense_ids", "expense_ids.state", "expense_ids.total_amount")
    def _compute_expense_to_report(self):
        """
        Compute the total amount of expenses to report for each record.

        Args:
            self (Recordset): The recordset of the current records.

        Returns:
            None
        """
        for record in self:
            # Filter the expenses that are in draft state and related to the current record
            report_expenses = record.expense_ids.filtered(
                lambda expense: expense.state == "draft"
                and expense.petty_cash_management_id == record
            )
            # Sum the total amount of the report expenses
            record.expense_to_report = sum(report_expenses.mapped("total_amount"))

    # Expenses to approve state is in reported
    @api.depends("expense_ids", "expense_ids.state", "expense_ids.total_amount")
    def _compute_expenses_to_approve(self):
        """
        Compute the total amount of expenses that need to be approved for each record.
        """
        for record in self:
            # Filter the expenses that are reported and belong to the current
            # record's petty cash management
            approve_expenses = record.expense_ids.filtered(
                lambda expense: expense.state == "reported"
                and expense.petty_cash_management_id == record
            )
            # Sum the total amount of the approved expenses and assign it
            # to the field expenses_to_approve
            record.expenses_to_approve = sum(approve_expenses.mapped("total_amount"))

    # Expenses to reimburse state is in approved
    @api.depends("expense_ids", "expense_ids.state", "expense_ids.total_amount")
    def _compute_expense_to_reimburse(self):
        """Compute the total amount of expenses to reimburse"""
        for record in self:
            # Filter the approved expenses related to the petty cash management record
            reimburse_expenses = record.expense_ids.filtered(
                lambda expense: expense.state == "approved"
                and expense.petty_cash_management_id == record
            )
            # Sum the total amounts of the approved expenses
            record.expenses_to_reimburse = sum(
                reimburse_expenses.mapped("total_amount")
            )

    # Operation in Cash on hands
    @api.depends("expense_ids", "expense_ids.state", "expense_ids.total_amount")
    def _total_cash_amount(self):
        """
        Calculate the total cash amount by subtracting all expenses from the cash amount.
        """
        # Calculate the total cash amount
        self.cash_on_hand = (
            self.cash_amount
            - self.expense_to_report
            - self.expenses_to_approve
            - self.expenses_to_reimburse
        )
