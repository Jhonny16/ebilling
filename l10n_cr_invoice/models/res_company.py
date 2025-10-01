# -*- coding: utf-8 -*-

from odoo import models, fields, api, Command
from odoo.exceptions import UserError
from ..hacienda_api import get_economic_activities
import json
import logging
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    setting_id = fields.Many2one('cr.ce.setting', string="Configuración Comprobante Electrónico")
    l10n_cr_economic_activity_ids = fields.Many2many('ce.economic.activity', string="Economic Activities")
    l10n_cr_provider_system = fields.Char(help='Proveedor de sistemas para emisión de Comprobantes',
                                          string="Provider System")
    l10n_cr_auth_user = fields.Char(string="Usuario de API", tracking=True)
    l10n_cr_auth_pass = fields.Char(string="Password de API")
    l10n_cr_test_env = fields.Boolean(
        string='Test environment',
        help='Enable the usage of test credentials',
        default=True)

    def l10n_cr_get_economic_activity(self):
        if not self.vat:
            return False

        response, vals = get_economic_activities(self.vat)
        if response.status_code in (200, 202) and len(response._content) > 0:
            content = json.loads(str(response._content, 'utf-8'))
            if content.get('actividades'):
                activities = content.get('actividades')
                if len(activities) < 1:
                    raise UserError("No se encontraron actividades económicas para la identificación: " + str(self.vat))

                EconomicActivity = self.env['ce.economic.activity']
                for a in activities:
                    search_ae = EconomicActivity.search([('code', '=', a['codigo'])])

                    if search_ae:
                        self.l10n_cr_economic_activity_ids = [Command.set(search_ae.ids)]
                    else:
                        activity = EconomicActivity.create({
                            'code': a['codigo'],
                            'name': a['descripcion'],
                        })
                        self.l10n_cr_economic_activity_ids = [Command.set(activity.ids)]
        else:
            output = 'Codigo: ' + str(
                response.status_code) + ', Mensaje: ' + str(response._content.decode())
            _logger.error(output)

    def l10n_cr_action_view_economic_activity(self):
        self.ensure_one()
        action = self.env.ref("l10n_cr_invoice.action_res_caecr").read()[0]
        if self.l10n_cr_economic_activity_ids:
            action["views"] = [(self.env.ref("l10n_cr_invoice.view_res_caecr_tree").id, "list"),
                               (self.env.ref("l10n_cr_invoice.view_res_caecr_form").id, "form")]
            action["domain"] = [('id', 'in', self.l10n_cr_economic_activity_ids.ids)]
        else:
            action = {"type": "ir.actions.act_window_close"}

        return action
