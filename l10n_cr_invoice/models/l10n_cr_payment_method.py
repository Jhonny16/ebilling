# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class L10nCrPaymentMethod(models.Model):
    _name = "l10n_cr.payment_method"
    _description = "Payment Method"

    def _get_l10n_cr_payment_method(self):
        """ Return the list of payment method codes required by Hacienda. """
        return [
            ("01", _("01 - Efectivo")),
            ("02", _("02 - Tarjeta")),
            ("03", _("03 - Cheque")),
            ("04", _("04 - Transferencia – depósito bancario")),
            ("05", _("05 - Recaudado por terceros")),
            ("06", _("06 - SINPE MOVIL")),
            ("07", _("07 - Plataforma Digital")),
            ("99", _("99 - Otros (se debe indicar el medio de pago)")),
        ]

    code = fields.Selection(string="Código Medio de Pago CR", selection="_get_l10n_cr_payment_method")
    name = fields.Char()

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"({record.code}) {record.name}"
