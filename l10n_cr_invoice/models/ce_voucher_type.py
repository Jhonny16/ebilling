# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class VoucherType(models.Model):
    _name = "ce.voucher.type"
    _description = "Tipo de documento"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    active = fields.Boolean(default=True)
    internal_type = fields.Selection(
        selection=[('invoice', 'Invoices'),
                   ('debit_note', 'Debit Notes'),
                   ('credit_note', 'Credit Notes')])
    move_type = fields.Selection(
        selection=[
            ('out_invoice', 'Customer Invoice'),
            ('in_invoice', 'Vendor Bill'),
            ('out_receipt', 'Out Receipt'),
            ('mh', 'Ministerio Hacienda'),
        ],
        string='Type',
    )

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"({record.code}) {record.name}"
