# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError, UserError
from ..hacienda_api import get_exoneration_info, get_economic_activities, get_exoneration_data
import json
import logging

_logger = logging.getLogger(__name__)

DESCRIPTION_INSTITUTION_CODE = [
    ('01', 'Ministerio de Hacienda'),
    ('02', 'Ministerio de Relaciones Exteriores y Culto'),
    ('03', 'Ministerio de Agricultura y Ganadería'),
    ('04', 'Ministerio de Economía, Industria y Comercio'),
    ('05', 'Cruz Roja Costarricense'),
    ('06', 'Asociación Obras del Espíritu Santo'),
    ('07', 'Asociación Obras del Espíritu Santo'),
    ('08', 'Federación Cruzada Nacional de protección al Anciano (Fecrunapa)'),
    ('09', 'Escuela de Agricultura de la Región Húmeda (EARTH)'),
    ('10', 'Instituto Centroamericano de Administración de Empresas (INCAE)'),
    ('11', 'Instituto Centroamericano de Administración de Empresas (INCAE)'),
    ('12', 'Autoridad Reguladora de los Servicios Públicos (Aresep)'),
    ('99', 'Otros'),
]


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    commercial_name = fields.Char()
    identification_id = fields.Many2one("ce.identification.type", required=False, string="Identification Type")
    l10n_cr_activity_id = fields.Many2one("ce.economic.activity", string="Economic Activity")

    # === Exonerations fields === #
    l10n_cr_exoneration_authorization = fields.Boolean('Exoneration or Authorization')
    l10n_cr_document_type_id = fields.Many2one('ce.exoneration.type',
                                               string='Tipo de Documento de Exoneracion o Autorizacion')
    l10n_cr_institution_name = fields.Selection(DESCRIPTION_INSTITUTION_CODE, 'Nombre de Institucion',
                                                help="NOTA 23: ANEXOS y ESTRCUTURAS")
    l10n_cr_exoneration_name = fields.Char(string='Nombre')
    l10n_cr_document_number = fields.Char('Numero de Documento', size=17)
    l10n_cr_issue_date = fields.Datetime('Fecha de Emision')
    l10n_cr_percentage_exoneration = fields.Float(
        string="Percentage Exoneration",
        default=0.00
    )
    l10n_cr_date_expiration = fields.Date(
        string="Expiration Date"
    )
    l10n_cr_allowed_cabys_ids = fields.One2many(
        comodel_name='res.partner.cabys.line',
        inverse_name='parent_id',
        string='Allowed CABYS Codes'
    )
    l10n_cr_exoneration_state = fields.Selection([('active', 'Active'),
                                                  ('close_to_expiring', 'Close to expiring'),
                                                  ('expired', 'Expired')], default='active',
                                                 compute="_compute_l10n_cr_exoneration_state")

    # === COMPUTE METHODS ===#

    tax_id = fields.Many2one('account.tax', string='Impuesto de exoneración')

    @api.depends("l10n_cr_date_expiration")
    def _compute_l10n_cr_exoneration_state(self):
        for partner in self:
            if partner.l10n_cr_date_expiration and partner.l10n_cr_date_expiration <= (
                    date.today() - timedelta(days=8)):
                partner.l10n_cr_exoneration_state = 'close_to_expiring'
            elif partner.l10n_cr_date_expiration and partner.l10n_cr_date_expiration <= date.today():
                partner.l10n_cr_exoneration_state = 'expired'
            else:
                partner.l10n_cr_exoneration_state = 'active'

    # === BUSINESS METHODS ===#

    def l10n_cr_get_economic_activity(self):
        if not self.vat:
            return False

        response, vals = get_economic_activities(self.vat)
        if response.status_code in (200, 202) and len(response._content) > 0:
            content = json.loads(str(response._content, 'utf-8'))
            if content.get('actividades'):
                activities = content.get('actividades')
                if not len(activities):
                    raise UserError("No se encontraron actividades económicas para la identificación: " + str(self.vat))

                EconomicActivity = self.env['ce.economic.activity']
                activity = activities[0]
                search_ae = EconomicActivity.search([('code', '=', activity['codigo'])], limit=1)
                if activity:
                    self.l10n_cr_activity_id = search_ae.id
                else:
                    activity = EconomicActivity.create({
                        'code': activity['codigo'],
                        'name': activity['descripcion'],
                    })
                    self.l10n_cr_activity_id = [Command.set(activity.ids)]
        else:
            output = 'Codigo: ' + str(
                response.status_code) + ', Mensaje: ' + str(response._content.decode())
            _logger.error(output)

    @api.constrains('l10n_cr_percentage_exoneration')
    def _check_l10n_cr_percentage_exoneration(self):
        for partner in self:
            if partner.l10n_cr_percentage_exoneration < 0.00:
                raise ValidationError(_("The percentage exoneration cannot be negative."))

    # @api.onchange('l10n_cr_document_number')
    # def _onchange_exoneration_number(self):
    #     if self.l10n_cr_document_number:
    #         self.definir_informacion_exo(self.l10n_cr_document_number)
    def search_exoneration_document(self):
        self.ensure_one()
        if not self.l10n_cr_document_number:
            raise ValidationError("Ingres el N°Documento!")
        self.definir_informacion_exo(self.l10n_cr_document_number)

    def definir_informacion_exo(self, l10n_cr_document_number):
        """
        This method is used to define the exoneration information based on the document number.
        It can be overridden in custom modules to implement specific logic.
        """

        #response, vals = get_exoneration_info(l10n_cr_document_number)
        content = get_exoneration_data(l10n_cr_document_number)
        if content and 'identificacion' in content:
            if self.vat != content.get('identificacion'):
                _logger.error('El código de exoneración no concuerda con la cédula del socio de negocio.')
                return

            issue_date = datetime.strptime(str(content.get('fechaEmision'))[:10], '%Y-%m-%d')
            self.l10n_cr_issue_date = issue_date
            date_expiration = datetime.strptime(str(content.get('fechaVencimiento'))[:10], '%Y-%m-%d')
            self.l10n_cr_date_expiration = date_expiration
            self.l10n_cr_percentage_exoneration = float(content.get('porcentajeExoneracion'))
            self.l10n_cr_institution_name = content.get('CodigoInstitucion')

            document_type = content.get('tipoDocumento')
            exoneration_type_id = self.env["ce.exoneration.type"].search([('ce_code', '=', document_type.get('codigo'))], limit=1)
            if exoneration_type_id:
                self.l10n_cr_document_type_id = exoneration_type_id.id

            if content.get('cabys'):
                self.l10n_cr_allowed_cabys_ids = [Command.clear()]
                self.l10n_cr_allowed_cabys_ids = [Command.create({'exoneration_code': code, 'cabys_code': code}) for
                                                  code in content.get('cabys')]


class ResPartnerCabysLine(models.Model):
    _name = "res.partner.cabys.line"
    _description = "Allowed CABYS"

    parent_id = fields.Many2one(
        comodel_name='res.partner'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product"
    )
    cabys_code = fields.Char(
        string="CABYS Code",
        size=13
    )
    exoneration_code = fields.Char(
        string="Exoneration Code",
        size=13
    )

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id and self.product_id.product_cabys_id:
            self.cabys_code = self.product_id.product_cabys_id.code
            self.exoneration_code = self.product_id.product_cabys_id.code
