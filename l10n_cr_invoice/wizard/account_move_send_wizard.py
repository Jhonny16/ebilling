# -*- coding: utf-8 -*-

from odoo import models


class AccountMoveSendWizard(models.TransientModel):
    _inherit = 'account.move.send.wizard'

    def action_send_and_print(self, allow_fallback_pdf=False):
        # EXTENDS account - to mark the CE state_mail as sent .

        res = super().action_send_and_print(allow_fallback_pdf=allow_fallback_pdf)
        if res:
            move = self.move_id
            if move.country_code in ['CR'] and move.l10n_cr_fiscal_journal:
                if move.document_id and move.document_id.state == 'accepted':
                    move.document_id.state_mail = 'sent'
