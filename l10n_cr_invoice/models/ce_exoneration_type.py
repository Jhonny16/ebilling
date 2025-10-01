# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ExoAuthDocType(models.Model):
    _name = 'ce.exoneration.type'
    _description = 'Exoneration or Authorization Document Type'

    name = fields.Char(required=True)
    ce_code = fields.Char('Code', size=2, required=True)

    @api.depends('ce_code', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"({record.ce_code}) {record.name}"
