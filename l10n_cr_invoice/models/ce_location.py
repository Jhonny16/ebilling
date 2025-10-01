# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CRLocation(models.Model):
    _name = "ce.location"
    _description = "Sucursal de la empresa"

    name = fields.Char(string="Sucursal", required=True, copy=False)
    description = fields.Char(help="Nombre comercial en caso que difiera del nombre real.", copy=False)
    code = fields.Char(required=True, size=3, copy=False,
                       help="001 para Sede Principal, 002 para Primera Tienda, etc.")
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id)', 'Código único por Compañia!'),
    ]
