# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountTax(models.Model):
    _inherit = "account.tax"

    def _get_l10n_cr_taxes_code(self):
        """ Return the list of taxes codes required by Hacienda. """
        return [
            ("01", "01 - Impuesto al Valor Agregado"),
            ("02", "02 - Impuesto Selectivo de Consumo"),
            ("03", "03 - Impuesto Único a los Combustibles"),
            ("04", "04 - Impuesto específico de Bebidas Alcohólicas"),
            ("05", "05 - Impuesto Específico sobre las bebidas envasadas sin contenido alcohólico y jabones de tocador"),
            ("06", "06 - Impuesto a los Productos de Tabaco"),
            ("07", "07 - IVA (cálculo especial)"),
            ("08", "08 - IVA Régimen de Bienes Usados (Factor)"),
            ("12", "12 - Impuesto Específico al Cemento"),
            ("99", "99 - Otros"),
        ]

    def _get_l10n_cr_iva_tax_rate(self):
        """ Return the list of IVA taxes rates and codes  required by Hacienda. """
        return [
            ("01", "01 - Tarifa 0% (Exento)"),
            ("02", "02 - Tarifa reducida 1%"),
            ("03", "03- Tarifa reducida 2%"),
            ("04", "04- Tarifa reducida 4%"),
            ("05", "05 - Transitorio 0%"),
            ("06", "06 - Transitorio 4%"),
            ("07", "07 - Transitorio 8%"),
            ("08", "08 - Tarifa general 13%"),
            ("09", "09 - Tarifa reducida 0.5%)"),
            ("10", "10 - Tarifa Exenta"),
            ("11", "11 - Tarifa 0% sin derecho a crédito"),
        ]

    code_cr = fields.Selection(string="Código de impuesto", selection="_get_l10n_cr_taxes_code")
    iva_tax_rate = fields.Selection(string="IVA Tax Rate", selection="_get_l10n_cr_iva_tax_rate")
    is_exonerated = fields.Boolean(string='Usado para exoneración')
