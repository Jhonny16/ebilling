# -*- coding: utf-8 -*-

from odoo import _, fields, models, api
from odoo.exceptions import ValidationError
import requests
from datetime import datetime, date

url = 'https://api.hacienda.go.cr/fe/ex?autorizacion='

_DOCUMENT_TYPE = [
    ('01', 'Compras autorizadas por la Dirección General de Tributación'),
    ('02', 'Ventas exentas a diplomáticos'),
    ('03', 'Autorizado por Ley Especial'),
    ('04', 'Exenciones Dirección General de Hacienda Autorización Local Genérica'),
    ('05', 'Exenciones Dirección General de Hacienda Transitorio V (servicios de ingeniería, arquitectura, topografía obra civil)'),
    ('06', 'Servicios turísticos inscritos ante el Instituto Costarricense de Turismo (ICT)'),
    ('07', 'Transitorio XVII (Recolección, Clasificación, almacenamiento de Reciclaje y reutilizable)'),
    ('08', 'Exoneración a Zona Franca'),
    ('09', 'Exoneración de servicios complementarios para la exportación articulo 11 RLIVA'),
    ('10', 'Órgano de las corporaciones municipales'),
    ('11', 'Exenciones Dirección General de Hacienda Autorización de Impuesto Local Concreta'),
    ('99', 'Otros'),
]

class ResPartnerExonerated(models.Model):
    _name = "res.partner.exonerated"
    _description = 'Exoneración de clientes'
    _rec_name = 'document_number'

    partner_id = fields.Many2one('res.partner', string='Cliente')
    vat = fields.Char('Doc.Identificación')
    document_number = fields.Char(string='Número de documento')
    identification = fields.Char(string='Identificación')
    project_code = fields.Char(string='Código proyecto CFIA')
    exoneration_percentage = fields.Float(string='Porcentaje exoneración')
    authorization_code = fields.Char(string='Autorización')
    authorization_type = fields.Char(string='Tipo autorización')
    document_type = fields.Selection(_DOCUMENT_TYPE, string='Tipo documento')
    date_emission = fields.Date(string='Fecha emisión')
    date_due = fields.Date(string='Fecha vencimiento')
    year = fields.Char(string='Año')
    cabys = fields.Text(string='Cabys')
    institution_code = fields.Char(string='Código institución')
    institution_nombre = fields.Char(string='Nombre institución')
    cabys_has = fields.Boolean(string='Posee Cabys')

    def search_exoneration(self):
        res = {}
        if not self.partner_id:
            raise ValidationError(_("Seleccione primero un cliente."))
        if self.document_number:
            data = self.find_data()
            if 'document_number' in data:
                self.sudo().write(data)
                res['warning'] = {'title': _('Bien!'), 'message': _('Datos encontrados!')}
                return res

    def find_data(self):
        """EXAMPLES"""
        #https://api.hacienda.go.cr/fe/ex?autorizacion=AL-00088689-22
        #https://api.hacienda.go.cr/fe/ex?autorizacion=AL-00088680-22

        res = {}
        url_compound = url + self.numero_documento

        try:
            result = requests.get(url_compound)
        except Exception as e:
            raise ValidationError(_("Error: %s " % e))

        try:
            if result.status_code == 200:
                res_json = result.json()
                document_number = res_json['numeroDocumento']
                identification = res_json['identificacion']
                project_code = res_json['codigoProyectoCFIA'] if 'codigoProyectoCFIA' in res_json else False
                exoneration_percentage = res_json['porcentajeExoneracion'] if 'porcentajeExoneracion' in res_json else False
                authorization_code = res_json['autorizacion'] if 'autorizacion' in res_json else False
                date_emission = datetime.strptime(res_json['fechaEmision'], "%Y-%m-%dT%H:%M:%S").date()
                date_due = datetime.strptime(res_json['fechaVencimiento'], "%Y-%m-%dT%H:%M:%S").date()
                year = res_json['ano'] if 'ano' in res_json else False
                cabys_list = res_json['cabys'] if 'cabys' in res_json else False
                cabys_text = ','.join(caby for caby in cabys_list)
                authorization_type = res_json['tipoAutorizacion'] if 'tipoAutorizacion' in res_json else False
                code_type = res_json['tipoDocumento']['codigo']
                document_type = _DOCUMENT_TYPE[code_type]
                institution_code =  res_json['CodigoInstitucion'] if 'CodigoInstitucion' in res_json else False
                institution_nombre =  res_json['nombreInstitucion'] if 'nombreInstitucion' in res_json else False
                cabys_has =  res_json['poseeCabys'] in [True, 'true'] if 'poseeCabys' in res_json else False


                data = {
                    'partner_id': self.partner_id.id,
                    #'vat': identificacion,
                    'document_number': document_number,
                    'identification': identification,
                    'project_code': project_code,
                    'exoneration_percentage': exoneration_percentage,
                    'authorization_code': authorization_code,
                    'authorization_type': authorization_type,
                    'document_type': document_type,
                    'date_emission': date_emission,
                    'date_due': date_due,
                    'year': year,
                    'institution_code': institution_code,
                    'institution_nombre': institution_nombre,
                    'cabys_has': cabys_has,
                    'cabys': cabys_text,
                }
                return data
            else:
                res['warning'] = {'title': _('Ups'), 'message': _('Documento de exoneración no encontrado !')}
                return res
        except Exception as e:
            raise ValidationError(_("Advertencia: %s", e))
