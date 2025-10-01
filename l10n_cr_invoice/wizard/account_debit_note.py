# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError
from datetime import datetime
import pytz


class AccountDebitNote(models.TransientModel):
    _inherit = "account.debit.note"

    @api.model
    def default_get(self, fields_list):
        result = super(AccountDebitNote, self).default_get(fields_list)
        default_doc_reference = self.env["ce.reference.document"].search([('code', '=', "02")], limit=1)
        default_code_reference = self.env["ce.reference.code"].search([('code', '=', "01")], limit=1)

        if not default_doc_reference:
            error_msg = _(
                "Not found Reference Document (02) - Nota de Débito Electrónica",
            )
            raise UserError(error_msg)

        if not default_code_reference:
            error_msg = _(
                "Not found Reference Code (01) - Anula Documento de Referencia",
            )
            raise UserError(error_msg)

        result['l10n_cr_tipo_doc_reference_id'] = default_doc_reference.id
        result['l10n_cr_cod_reference_id'] = default_code_reference.id

        return result

    l10n_cr_fiscal_journal = fields.Boolean(related='journal_id.l10n_cr_fiscal_journal')
    l10n_cr_tipo_doc_reference_id = fields.Many2one('ce.reference.document', string="Tipo de Documento Referencia")
    l10n_cr_cod_reference_id = fields.Many2one('ce.reference.code', string="Códigos de referencia")
    l10n_cr_voucher_type_id = fields.Many2one('ce.voucher.type', 'Voucher Type', ondelete='cascade', readonly=False,
                                              compute='_compute_l10n_cr_document_type')

    @api.depends('move_ids')
    def _compute_l10n_cr_document_type(self):
        for record in self:
            cd = self.env["ce.voucher.type"].search([('internal_type', '=', 'debit_note')])
            record.l10n_cr_voucher_type_id = cd[0]

    def _prepare_default_values(self, move):
        res = super(AccountDebitNote, self)._prepare_default_values(move)
        if self.country_code == 'CR':
            now_utc = datetime.now(pytz.timezone('UTC'))
            if move.l10n_cr_fiscal_journal:
                res.update(
                    dict(
                        voucher_type_id=self.l10n_cr_voucher_type_id.id,
                        tipo_doc_reference_id=self.l10n_cr_tipo_doc_reference_id.id,
                        cod_referencia_id=self.l10n_cr_cod_reference_id.id,
                        reason_ref=self.reason,
                        numero_ref=move.document_id.name,
                        terminal_id=move.terminal_id.id,
                        # journal_pay_ids=[Command.set(move.journal_pay_ids.ids)] if move.journal_pay_ids else [],
                        # l10n_cr_payment_method_ids=[Command.set(move.l10n_cr_payment_method_ids.ids)] if move.l10n_cr_payment_method_ids else [],
                        invoice_payment_term_id=move.invoice_payment_term_id.id,
                        date_issue_ref=now_utc.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )
                if move.l10n_cr_buyer_activity_id:
                    res.update({
                        'l10n_cr_buyer_activity_id': move.l10n_cr_buyer_activity_id.id,
                    })
                if move.l10n_cr_payment_method_ids:
                    res.update({
                        'l10n_cr_payment_method_ids': [Command.set(move.l10n_cr_payment_method_ids.ids)],
                    })

        return res
