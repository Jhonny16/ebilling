# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    l10n_cr_fiscal_journal = fields.Boolean(
        string="Fiscal Journal"
    )

    @api.model
    def _create_sequence(self, vals, refund=False):
        res = super(AccountJournal, self)._create_sequence(vals, refund)
        if vals.get('type') in ['sale', 'purchase'] or vals.get('refund_sequence_number_next'):
            res.update({'use_date_range': None})
        return res

    @api.constrains("l10n_cr_fiscal_journal")
    def _check_cr_fiscal_company(self):
        for journal in self:
            if journal.l10n_cr_fiscal_journal and not journal.company_id.vat:
                raise UserError(_("Company does not have a VAT defined"))
