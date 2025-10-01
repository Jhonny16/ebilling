# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class UoM(models.Model):
    _inherit = "uom.uom"

    code = fields.Char()
    l10n_cr_uom_type = fields.Selection([('product', 'Product'), ('service', 'Service')])


class UoMCategory(models.Model):
    _inherit = "uom.category"

    measure_type = fields.Selection([
        ('unit', 'Default Units'),
        ('weight', 'Default Weight'),
        ('working_time', 'Default Working Time'),
        ('length', 'Default Length'),
        ('volume', 'Default Volume'),
        ('area', 'Area'),
        ('services', 'Services'),
        ('rent', 'Rent'),
    ], string="Type of Measure")
