# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CodeTypeProduct(models.Model):
    _name = "code.type.product"
    _description = "Code Type Product"

    code = fields.Char()
    name = fields.Char()

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"({record.code}) {record.name}"
