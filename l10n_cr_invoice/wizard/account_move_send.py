# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveSend(models.AbstractModel):
    _inherit = 'account.move.send'

    # -------------------------------------------------------------------------
    # ATTACHMENTS
    # -------------------------------------------------------------------------

    @api.model
    def _get_invoice_extra_attachments(self, move):
        """
                :returns: object (ir.attachment)
                """
        # EXTENDS 'account'

        # we require these to be downloadable for a better UX. It was also said that the xml and pdf files are
        # important files that needs to be shared with the customer.

        attachments = super()._get_invoice_extra_attachments(move)
        if move.country_code == 'CR' and move.l10n_cr_fiscal_journal:
            if move.document_id and move.document_id.xml_file and move.document_id.state == 'accepted':
                doc = move.document_id
                ir_attachment = self.env['ir.attachment'].sudo()
                attachment_vals = {'name': str(doc.xml_file_name),
                                   'datas': doc.xml_file,
                                   'res_id': move.id,
                                   'res_model': "account.move",
                                   'type': 'binary',
                                   'res_field': 'xml_file',
                                   }
                att = ir_attachment.create(attachment_vals)
                attachments |= att
            if move.document_id and move.document_id.xml_mh_file and move.document_id.state == 'accepted':
                doc = move.document_id
                ir_attachment = self.env['ir.attachment'].sudo()
                attachment_vals = {'name': str(doc.xml_mh_file_name),
                                   'datas': doc.xml_mh_file,
                                   'res_id': move.id,
                                   'res_model': "account.move",
                                   'type': 'binary',
                                   'res_field': 'xml_mh_file',
                                   }
                att = ir_attachment.create(attachment_vals)
                attachments |= att

        return attachments
