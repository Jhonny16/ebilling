# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EconomicActivity(models.Model):
    _name = 'ce.economic.activity'
    _description = 'Economic Activity'
    _order = 'sequence'

    code = fields.Char(required=True, help='Economic Activity Code')
    name = fields.Char('Activity', required=True, help='Economic Activity Name')
    sequence = fields.Integer()
    active = fields.Boolean(default=True)

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"({record.code}) {record.name}"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """ search in name, code and category"""
        args = args or []
        # search in name and code
        domain = args + ['|', ('name', operator, name), ('code', operator, name)]
        activities = self.search_fetch(
            domain, ['display_name'], limit=limit,
        )
        return [(activity.id, activity.display_name) for activity in activities]
