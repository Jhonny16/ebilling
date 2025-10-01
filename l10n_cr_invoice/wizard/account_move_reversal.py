# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError
from datetime import datetime
import pytz


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    @api.model
    def default_get(self, fields_list):
        result = super(AccountMoveReversal, self).default_get(fields_list)

        move_reference = self.env["account.move"]
        if result.get('move_ids'):
            move_reference = self.env["account.move"].browse(result.get('move_ids')[0][2][0])

        doc_reference = "03" if (move_reference and move_reference.move_type in ['out_invoice']) else "17"
        default_doc_reference = self.env["ce.reference.document"].search([('code', '=', doc_reference)], limit=1)
        default_code_reference = self.env["ce.reference.code"].search([('code', '=', "01")], limit=1)

        if not default_doc_reference:
            error_msg = _(
                f"Not found Reference Document ({default_doc_reference.code}) - {default_doc_reference.name}",
            )
            raise UserError(error_msg)

        if not default_code_reference:
            error_msg = _(
                f"Not found Reference Code ({default_code_reference.code}) - {default_code_reference.name}",
            )
            raise UserError(error_msg)

        result['l10n_cr_tipo_doc_reference_id'] = default_doc_reference.id
        result['l10n_cr_cod_reference_id'] = default_code_reference.id
        return result

    l10n_cr_fiscal_journal = fields.Boolean(related='journal_id.l10n_cr_fiscal_journal')
    l10n_cr_tipo_doc_reference_id = fields.Many2one('ce.reference.document', string="Tipo de Documento Referencia")
    l10n_cr_cod_reference_id = fields.Many2one('ce.reference.code', string="Códigos de referencia")
    l10n_cr_voucher_type_id = fields.Many2one('ce.voucher.type', 'Voucher Type', ondelete='cascade',
                                              compute='_compute_l10n_cr_document_type', readonly=False)

    @api.model
    def _reverse_type_map(self, move_type):
        match = {
            'entry': 'entry',
            'out_invoice': 'out_refund',
            'in_invoice': 'in_refund',
            'in_refund': 'in_invoice',
            'out_receipt': 'in_receipt',
            'in_receipt': 'out_receipt',
        }
        return match.get(move_type)

    @api.depends('move_ids')
    def _compute_l10n_cr_document_type(self):
        for record in self:
            refund = record.env['account.move'].new({
                'move_type': record._reverse_type_map(record.move_ids.move_type),
                'journal_id': record.move_ids.journal_id.id,
                'partner_id': record.move_ids.partner_id.id,
                'company_id': record.move_ids.company_id.id,
            })
            record.l10n_cr_voucher_type_id = refund.voucher_type_id

    def _prepare_default_reversal(self, move):
        """ Set the default document type and number in the new revsersal move taking into account the ones selected in
        the wizard """
        res = super()._prepare_default_reversal(move)
        if self.country_code == 'CR' and move.l10n_cr_fiscal_journal:
            now_utc = datetime.now(pytz.timezone('UTC'))
            res.update({
                'voucher_type_id': self.l10n_cr_voucher_type_id.id,
                'tipo_doc_reference_id': self.l10n_cr_tipo_doc_reference_id.id,
                'cod_referencia_id': self.l10n_cr_cod_reference_id.id,
                'reason_ref': self.reason or "Reversal of: " + move.document_id.name,
                'date_issue_ref': now_utc.strftime("%Y-%m-%d %H:%M:%S"),
                'numero_ref': move.document_id.name,
                'terminal_id': move.terminal_id.id,
                # 'journal_pay_ids': [Command.set(move.journal_pay_ids.ids)] if move.journal_pay_ids else [],
                # 'l10n_cr_payment_method_ids': [Command.set(move.l10n_cr_payment_method_ids.ids)] if move.l10n_cr_payment_method_ids else [],
                'invoice_payment_term_id': move.invoice_payment_term_id.id,
            })
            if move.l10n_cr_buyer_activity_id:
                res.update({
                    'l10n_cr_buyer_activity_id': move.l10n_cr_buyer_activity_id.id,
                })
            if move.l10n_cr_payment_method_ids:
                res.update({
                    'l10n_cr_payment_method_ids': [Command.set(move.l10n_cr_payment_method_ids.ids)],
                })

        return res
