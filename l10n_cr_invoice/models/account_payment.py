# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    l10n_cr_payment_method_id = fields.Many2one(related='move_id.l10n_cr_payment_method_id', readonly=False)

    def l10n_cr_receipt_payment_send(self, payment_date, memo):
        move_id = self.move_id
        self.move_id.l10n_cr_receipt_payment_send(payment_date, memo)
