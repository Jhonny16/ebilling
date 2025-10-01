# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    l10n_cd_commercial_measurement = fields.Char(string="Unidad de Medida Comercial")
    l10n_sv_tariff_item = fields.Char(string="Partida arancelaria", size=12,
                                      help="Partida arancelaria para factura de exportación")

    @api.model
    def _default_code_type_id(self):
        code_type_id = self.env['code.type.product'].search([('code', '=', '04')], limit=1)
        return code_type_id or False

    l10n_cr_code_type_id = fields.Many2one(comodel_name="code.type.product", string="Tipo de código",
                                           default=_default_code_type_id)
