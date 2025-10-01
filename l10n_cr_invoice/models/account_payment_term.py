# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    payment_type_id = fields.Many2one("ce.payment.term.type", string="Tipo de pago CR")
