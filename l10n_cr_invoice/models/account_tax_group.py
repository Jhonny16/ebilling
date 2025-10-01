# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class AccountTaxGroup(models.Model):

    _inherit = 'account.tax.group'

    l10n_cr_billing_indicator = fields.Selection([
        ('01', 'Contribución parafiscal'),
        ('02', 'Timbre de la Cruz Roja'),
        ('03', 'Timbre de Benemérito Cuerpo de Bomberos de Costa Rica'),
        ('04', 'Cobro de un tercero'),
        ('05', 'Costos de Exportación'),
        ('06', 'Impuesto de servicio 10%'),
        ('08', 'Timbre de Colegios Profesionales'),
        ('99', 'Otros Cargos'),
    ], string='Billing Indicator')
