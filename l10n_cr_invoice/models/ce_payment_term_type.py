# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PaymentTermType(models.Model):
    _name = "ce.payment.term.type"
    _description = "Tipos de Termino de Pago"
    _order = "code asc"

    active = fields.Boolean(default=True)
    code = fields.Char()
    name = fields.Char()

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"({record.code}) {record.name}"
