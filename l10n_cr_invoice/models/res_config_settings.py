# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from ..hacienda_api import HaciendaApi
from odoo.exceptions import ValidationError
import requests


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_l10n_cr_partner_autocomplete = fields.Boolean("Hacienda Partner Autocomplete",
                                                         config_parameter='l10n_cr_partner_autocomplete.hacienda_autocomplete')
    l10n_cr_provider_system = fields.Char(related='company_id.l10n_cr_provider_system', readonly=False)
    l10n_cr_test_env = fields.Boolean(related='company_id.l10n_cr_test_env', readonly=False)
    l10n_cr_auth_user = fields.Char(related='company_id.l10n_cr_auth_user', readonly=False)
    l10n_cr_auth_pass = fields.Char(related='company_id.l10n_cr_auth_pass', readonly=False)
    l10n_cr_setting_id = fields.Many2one(related='company_id.setting_id', readonly=False)

    def l10n_cr_action_verify(self):
        self.ensure_one()
        hacienda_api = HaciendaApi(company_id=self.company_id)
        try:
            kernel = hacienda_api.getToken()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'info',
                    'sticky': False,
                    'message': "%s" % kernel,
                }
            }

        except requests.exceptions.MissingSchema:
            raise ValidationError(_("Wrong external service URL"))

        except requests.exceptions.ConnectionError:
            raise ValidationError(_("Check you connection"))
