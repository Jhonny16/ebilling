# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class IdentificationType(models.Model):
    _name = "ce.identification.type"
    _description = "Identificacion de la Empresa"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    notes = fields.Text(required=True)
    active = fields.Boolean(default=True)
