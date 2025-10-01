# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError, RedirectWarning
from io import BytesIO
from . import FE
from . import TE
from . import ND
from . import NC
from . import FEE
from . import FEC
from . import REP
from datetime import datetime, timedelta
from ..hacienda_api import HaciendaApi, HACIENDA_RESOLUTION_URL, HACIENDA_NAMESPACE_URL
from collections import defaultdict
import xml.etree.ElementTree as ET
import pytz
import base64
import phonenumbers
import qrcode
import re
import subprocess
import tempfile
import logging
_logger = logging.getLogger(__name__)

L10N_CR_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
VOUCHER_TYPE_XMLNS = {
    '01': 'facturaElectronica',
    '02': 'notaDebitoElectronica',
    '03': 'notaCreditoElectronica',
    '04': 'tiqueteElectronico',
    '05': 'mensajeReceptor',
    '06': 'mensajeReceptor',
    '07': 'mensajeReceptor',
    '08': 'facturaElectronicaCompra',
    '09': 'facturaElectronicaExportacion',
    '10': 'reciboElectronicoPago',
}
VOUCHER_TYPE_ABBR = {
    '01': 'FE',
    '02': 'ND',
    '03': 'NC',
    '04': 'TE',
    '05': 'CCE',
    '06': 'CPCE',
    '07': 'RCE',
    '08': 'FEC',
    '09': 'FEE',
    '10': 'REP',
}

L10N_CR_DESCRIPTION_DISCOUNT_TYPE_CODE_MAP = {
    '01': 'Descuento por Regalía',
    '02': 'Descuento por Regalía IVA Cobrado al Cliente',
    '03': 'Descuento por Bonificación',
    '04': 'Descuento por volumen',
    '05': 'Descuento por Temporada (estacional)',
    '06': 'Descuento promocional',
    '07': 'Descuento Comercial',
    '08': 'Descuento por frecuencia',
    '09': 'Descuento sostenido',
    '10': 'Otros descuentos',
}


class Document(models.Model):
    _name = "ce.document"
    _rec_name = "number"
    _description = "Electronic Voucher"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = "create_date desc"

    TYPE_INVOICE = [
        ('out_invoice', 'Cliente'),
        ('in_invoice', 'Proveedor'),
        ('out_refund', 'Reembolso Cliente'),
        ('in_refund', 'Reembolso Proveedor'),
        ('out_ticket', 'Ticket Cliente'),
        ('in_ticket', 'Ticket Proveedor'),
        ('out_receipt', 'Out Receipt'),
    ]

    @api.model
    def default_get(self, fields_list):
        result = super(Document, self).default_get(fields_list)
        force_economic_activity = self.env.context.get('force_economic_activity')
        if force_economic_activity:
            result['economic_activity_id'] = force_economic_activity
        else:
            economic_activity_ids = self.env.company.l10n_cr_economic_activity_ids
            result['economic_activity_id'] = economic_activity_ids and economic_activity_ids[0].id or False

        return result

    name = fields.Char(string="Clave", copy=False, readonly=True)
    state = fields.Selection(selection=[('pending', "Pendiente"),
                                        ('sent', "Enviado"),
                                        ('accepted', "Aceptado"),
                                        ('partially', 'Parcialmente Aceptado'),
                                        ('denied', 'Rechazado')],
                             string="State", default='pending', copy=False, help="States for use internal.")
    state_mail = fields.Selection(
        selection=[('not_sent', 'No enviado'),
                   ('sent', 'Enviado'),
                   ('not_mail', 'Sin Correo')], string="Estado Correo",
        default='not_sent', copy=False)
    invoice_id = fields.Many2one('account.move', string="Invoice", copy=False, readonly=True, ondelete='restrict')
    invoice_name = fields.Char(related='invoice_id.name', string="Invoice", copy=False)
    invoice_type = fields.Selection(selection=TYPE_INVOICE, string="Internal Type", copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', string="Empresa", copy=False, readonly=True)
    terminal_id = fields.Many2one('ce.terminal', string="Terminal", copy=False, readonly=True)
    location_id = fields.Many2one('ce.location', related="terminal_id.location_id", string="Lugar", store=True,
                                  readonly=True, copy=False)
    company_id = fields.Many2one('res.company', string="Company", readonly=True, copy=False)
    economic_activity_id = fields.Many2one('ce.economic.activity', string="Economic Activity", ondelete="restrict")
    l10n_cr_buyer_activity_id = fields.Many2one('ce.economic.activity', string="Buyer Activity", ondelete="restrict")
    voucher_type_id = fields.Many2one("ce.voucher.type", string="Voucher Type",
                                      copy=False, readonly=True,
                                      ondelete="restrict")
    voucher_type_code = fields.Char(related="voucher_type_id.code", string="Código del Tipo de documento", copy=False)
    currency_id = fields.Many2one('res.currency', readonly=True, string='Currency')
    payment_term_type_id = fields.Many2one("ce.payment.term.type", "Condición de venta")
    xml_amount_tax = fields.Monetary(string="Impuesto", compute='_amount_total', store=True,
                                     copy=False, currency_field='currency_id')
    xml_amount_total = fields.Monetary(string="Importe total", compute='_amount_total', store=True,
                                       copy=False, currency_field='currency_id')
    situation = fields.Selection(
        selection=[('normal', 'Normal'),
                   ('contingency', 'Contingencia'),
                   ('no_internet', 'Sin Internet')],
        string="Status Voucher", required=True, default='normal', copy=False, readonly=True)
    xml_file = fields.Binary(string="Archivo XML", attachment=True, copy=False)
    xml_file_name = fields.Char(string="Nombre Archivo XML", copy=False)
    xml_mr_file = fields.Binary(string="Archivo XML MR", attachment=True, copy=False)
    xml_mr_file_name = fields.Char(string="Nombre Archivo XML MR", copy=False)
    date_issue = fields.Datetime(copy=False)
    date_issue_ref = fields.Datetime(copy=False)
    ind_state = fields.Selection(selection=[
        ('not_sent', "No Enviado"),
        ('recibido', "Recibido"),
        ('aceptado', "Aceptado"),
        ('rechazado', "Rechazado"),
        ('error', "Error"),
        ('procesando', "Procesando")],
        string="Hacienda State", default='not_sent', copy=False)
    number = fields.Char(string="Consecutive", copy=False, readonly=True)
    xml_mh_file = fields.Binary(string="Archivo XML MH", attachment=True, copy=False)
    xml_mh_file_name = fields.Char(string="Nombre Archivo XML MH", copy=False)
    message_detail = fields.Text(string="Detalle del Mensaje", copy=False)

    # help to reference the current rejected document
    ref_ids = fields.Many2many('ce.reference', string='Reference Documents')
    is_ref = fields.Boolean(default=False, help="Indicates whether the document is a substitute for a rejected invoice")

    # QR
    QR_code = fields.Binary(string="Code QR", readonly=True, copy=False)

    # === COMPUTE METHODS ===#

    @api.depends('invoice_id')
    def _amount_total(self):
        for env in self:
            if env.invoice_id:
                env.xml_amount_total = env.invoice_id.amount_total
                env.xml_amount_tax = env.invoice_id.amount_tax
                env.invoice_id = env.invoice_id.id

    # ===== BUTTONS =====

    def action_gen_xml(self, reference_nc=None, forzar=False):
        company_id = self.company_id
        if not forzar and self.xml_file:
            raise UserError('Ya existe un XML')

        if not company_id.l10n_cr_economic_activity_ids:
            raise UserError(_("Not exist Economic Activity for this company."))

        ceconfig_id = company_id.setting_id or company_id.parent_id.setting_id
        if not ceconfig_id:
            action = self.env.ref("base.action_res_company_form")
            msg = _("Must be selected an Environment in a Company.")
            raise RedirectWarning(msg, action.id, _("Go to Setting"))

        now = datetime.now(pytz.timezone('America/Costa_Rica'))
        now = now.replace(microsecond=0)
        activity_code_sender = self.economic_activity_id.code
        provider_system = (company_id.l10n_cr_provider_system
                           if company_id.l10n_cr_provider_system
                           else company_id.partner_id.vat)
        voucher_type_code = self.voucher_type_code

        def get_condition_sale():
            # condition_sale = (self.invoice_id
            #                   and self.invoice_id.payment_term_type_id.code
            #                   or "01")
            condition_sale = self.payment_term_type_id.code or "01"
            return condition_sale

        if voucher_type_code == '01':
            rootTag = 'FacturaElectronica'
            classdoc = FE
            sender = self.gen_emisor(classdoc)
            receiver = self.gen_receptor(classdoc)
            cedoc = FE.FacturaElectronica(Clave=self.name,
                                          ProveedorSistemas=provider_system,
                                          CodigoActividadEmisor=activity_code_sender,
                                          NumeroConsecutivo=self.number,
                                          FechaEmision=now,
                                          Emisor=sender,
                                          Receptor=receiver,
                                          CondicionVenta=get_condition_sale(),
                                          )
            if self.l10n_cr_buyer_activity_id:
                cedoc.set_CodigoActividadReceptor(self.l10n_cr_buyer_activity_id.code)
            other_charges = self._get_other_charges(classdoc)
            if other_charges:
                cedoc.set_OtrosCargos(other_charges)
            cedoc = self._gen_detail_and_summary(cedoc, classdoc)
        if voucher_type_code == '04':
            rootTag = 'TiqueteElectronico'
            classdoc = TE
            sender = self.gen_emisor(classdoc)
            receiver = self.gen_receptor(classdoc)
            cedoc = TE.TiqueteElectronico(Clave=self.name,
                                          ProveedorSistemas=provider_system,
                                          CodigoActividadEmisor=activity_code_sender,
                                          NumeroConsecutivo=self.number,
                                          FechaEmision=now,
                                          Emisor=sender,
                                          Receptor=receiver,
                                          CondicionVenta=get_condition_sale(),
                                          )
            other_charges = self._get_other_charges(classdoc)
            if other_charges:
                cedoc.set_OtrosCargos(other_charges)
            cedoc = self._gen_detail_and_summary(cedoc, classdoc)
        if voucher_type_code == '02':
            rootTag = 'NotaDebitoElectronica'
            classdoc = ND
            sender = self.gen_emisor(classdoc)
            cedoc = ND.NotaDebitoElectronica(Clave=self.name,
                                             ProveedorSistemas=provider_system,
                                             CodigoActividadEmisor=activity_code_sender,
                                             NumeroConsecutivo=self.number,
                                             FechaEmision=now,
                                             Emisor=sender,
                                             CondicionVenta=get_condition_sale(),
                                             )
            receiver = self.gen_receptor(classdoc)
            cedoc.set_Receptor(receiver)
            if self.l10n_cr_buyer_activity_id:
                cedoc.set_CodigoActividadReceptor(self.l10n_cr_buyer_activity_id.code)
            other_charges = self._get_other_charges(classdoc)
            if other_charges:
                cedoc.set_OtrosCargos(other_charges)
            cedoc = self._gen_detail_and_summary(cedoc, classdoc)
            self._add_reference_information(cedoc, classdoc, reference_nc)
        if voucher_type_code == '03':
            rootTag = 'NotaCreditoElectronica'
            classdoc = NC
            sender = self.gen_emisor(classdoc)
            cedoc = NC.NotaCreditoElectronica(Clave=self.name,
                                              ProveedorSistemas=provider_system,
                                              CodigoActividadEmisor=activity_code_sender,
                                              NumeroConsecutivo=self.number,
                                              FechaEmision=now,
                                              Emisor=sender,
                                              CondicionVenta=get_condition_sale(),
                                              )
            receiver = self.gen_receptor(classdoc)
            cedoc.set_Receptor(receiver)
            if self.l10n_cr_buyer_activity_id:
                cedoc.set_CodigoActividadReceptor(self.l10n_cr_buyer_activity_id.code)
            other_charges = self._get_other_charges(classdoc)
            if other_charges:
                cedoc.set_OtrosCargos(other_charges)
            cedoc = self._gen_detail_and_summary(cedoc, classdoc)
            self._add_reference_information(cedoc, classdoc, reference_nc)
        if voucher_type_code == '08':
            rootTag = 'FacturaElectronicaCompra'
            activity_code_buyer = self.economic_activity_id.code
            classdoc = FEC
            sender = self.gen_emisor(classdoc)
            receiver = self.gen_receptor(classdoc)
            cedoc = FEC.FacturaElectronicaCompra(Clave=self.name,
                                                 ProveedorSistemas=provider_system,
                                                 CodigoActividadReceptor=activity_code_buyer,
                                                 NumeroConsecutivo=self.number,
                                                 FechaEmision=now,
                                                 Emisor=sender,
                                                 Receptor=receiver,
                                                 CondicionVenta=get_condition_sale(),
                                                 )
            other_charges = self._get_other_charges(classdoc)
            if other_charges:
                cedoc.set_OtrosCargos(other_charges)
            cedoc = self._gen_detail_and_summary(cedoc, classdoc)
            self._add_reference_information(cedoc, classdoc, None)
        if voucher_type_code == '09':
            rootTag = 'FacturaElectronicaExportacion'
            classdoc = FEE
            sender = self.gen_emisor(classdoc)
            cedoc = FEE.FacturaElectronicaExportacion(Clave=self.name,
                                                      ProveedorSistemas=provider_system,
                                                      CodigoActividadEmisor=activity_code_sender,
                                                      NumeroConsecutivo=self.number,
                                                      FechaEmision=now,
                                                      Emisor=sender,
                                                      CondicionVenta=get_condition_sale(),
                                                      )

            other_charges = self._get_other_charges(classdoc)
            if other_charges:
                cedoc.set_OtrosCargos(other_charges)
            receiver = self.gen_receptor(classdoc)
            cedoc = self._gen_detail_and_summary(cedoc, classdoc)
            cedoc.set_Receptor(receiver)
        if voucher_type_code == '10':
            rootTag = 'ReciboElectronicoPago'
            classdoc = REP
            sender = self.gen_emisor(classdoc)
            receiver = self.gen_receptor(classdoc)

            if get_condition_sale() not in ["09", "11"]:
                raise UserError("La condición de venta para el recibo electrónico de pago debe ser 09 - Pago de servicios prestado al Estado o 11 - Pago de venta a crédito en IVA hasta 90 días (Artículo 27, LIVA)")

            cedoc = REP.ReciboElectronicoPago(Clave=self.name,
                                              ProveedorSistemas=provider_system,
                                              NumeroConsecutivo=self.number,
                                              FechaEmision=now,
                                              Emisor=sender,
                                              Receptor=receiver,
                                              CondicionVenta=get_condition_sale(),
                                              )
            other_charges = self._get_other_charges(classdoc)
            if other_charges:
                cedoc.set_OtrosCargos(other_charges)
            cedoc = self._gen_detail_and_summary_rep(cedoc, classdoc)
            self._add_reference_information(cedoc, classdoc, None)
        self.set_additional_vals(cedoc, classdoc)
        xmlType = VOUCHER_TYPE_XMLNS[voucher_type_code]
        ns = HACIENDA_NAMESPACE_URL + xmlType + '"'
        file = tempfile.NamedTemporaryFile(delete=False)
        cedoc.export(file, 0, name_=rootTag, namespacedef_=ns, pretty_print=True)
        file.write(b'\n')
        file.close()
        now = now.strftime(L10N_CR_DATE_FORMAT)
        self.write({
            "date_issue": now,
        })
        return self.sign_doc(file.name, ceconfig_id)

    def action_send_to_hacienda(self):
        documents = self._l10n_cr_check_documents_for_send()
        for document in documents:
            document._send_xml_to_MH()

    def action_request_state_to_hacienda(self):
        documents = self._l10n_cr_check_documents_for_send()
        for document in documents:
            document._send_request_to_MH()

    def action_send_mail(self):
        self._send_mail()

    # === BUSINESS METHODS ===#

    def gen_emisor(self, classdoc):
        """Retorna la instancia del emisor

            :param object classdoc: Clase del tipo de documento.
            """
        voucher_type_code = self.voucher_type_code
        if not self.company_id.vat:
            raise ValidationError(_('Your company has not defined an NIF.'))
        if not self.company_id.name:
            raise ValidationError(_('Your company has not defined an Name.'))
        if not self.company_id.street or not len(str(self.company_id.street).strip()):
            action = self.env.ref("base.action_res_company_form")
            msg = _('Your company has not defined a street.')
            raise RedirectWarning(msg, action.id, _("Go to Companies"))
        if self.voucher_type_code == '08' or self.invoice_type == 'in_refund':
            partner_id = self.partner_id
        else:
            partner_id = self.company_id.partner_id
        sender_name = partner_id.name.replace('&', ' ')
        sender_name = self.limit(sender_name, 80)
        if not partner_id.identification_id:
            raise ValidationError(_('Your company has not defined a Tax Identification Number Type'))
        identification = classdoc.IdentificacionType(Tipo=partner_id.identification_id.code,
                                                     Numero=partner_id.vat)
        if (self.voucher_type_code != '08' and self.invoice_type != 'in_refund') and not partner_id.email:
            raise ValidationError(_('Your company has not defined an email which is mandatory'))

        if (self.voucher_type_code != '08' and self.invoice_type != 'in_refund') and ((partner_id.state_id.code is False) or
                (partner_id.canton_id.code is False) or
                (partner_id.distrito_id.code is False)):
            raise ValidationError(_('Your Company is missing some address required values (State, Canton or Distrito)'))

        if voucher_type_code == '10':
            sender = classdoc.EmisorType(Nombre=sender_name,
                                         Identificacion=identification,
                                         CorreoElectronico=partner_id.email)
        else:
            if voucher_type_code not in ['08']:
                if not partner_id.state_id:
                    raise ValidationError(_('The province of partner must be required.'))
                if partner_id.state_id:
                    if not partner_id.state_id.code:
                        raise ValidationError(
                            'La Provincia del cliente seleccionado no tiene codigo para Hacienda, favor corregir!')
                if not partner_id.canton_id:
                    raise ValidationError(_('Then canton of partner must be required.'))
                if partner_id.canton_id:
                    if not partner_id.canton_id.code:
                        raise ValidationError(
                            'El canton del cliente seleccionado no tiene codigo para Hacienda, favor corregir!')
                if not partner_id.distrito_id:
                    raise ValidationError(_('Then distrito of partner must be required.'))
                if partner_id.distrito_id:
                    if not partner_id.distrito_id.code:
                        raise ValidationError(
                            'El distrito del cliente seleccionado no tiene codigo para Hacienda, favor corregir!')

                location = classdoc.UbicacionType(Provincia=int(partner_id.state_id.code),
                                                  Canton=int(partner_id.canton_id.code),
                                                  Distrito=int(partner_id.distrito_id.code),
                                                  OtrasSenas=self.limit(partner_id.street or '', 250),
                                                  )

                if partner_id.neighborhood_id.name:
                    location.set_Barrio(self.limit(partner_id.neighborhood_id.name, 50))

            sender = classdoc.EmisorType(Nombre=sender_name,
                                         Identificacion=identification,
                                         Ubicacion=location if self.voucher_type_code != '08' else None,
                                         CorreoElectronico=self.voucher_type_code != '08' and partner_id.email or None)

            if partner_id.identification_id.code == '05':
                if not partner_id.street:
                    raise UserError("Al utilizar el código 05 de Identificación del Emisor debe estar presente el campo direccion")

                sender.set_OtrasSenasExtranjero(self.limit(partner_id.street or '', 250))

            # if self.voucher_type_code == '08' and partner_id.identification_id.code == '05':
            #     sender.set_Ubicacion(ubicacion)

        if voucher_type_code != '10' and partner_id.commercial_name:
            sender_commercial_name = partner_id.commercial_name.replace('&', ' ')
            sender.set_NombreComercial(self.limit(sender_commercial_name, 80))
        if voucher_type_code != '10' and (partner_id.phone or partner_id.mobile) and partner_id.identification_id.code != '05':
            tel = partner_id.phone if partner_id.phone else partner_id.mobile
            phone = phonenumbers.parse(tel, 'CR')
            sender.set_Telefono(classdoc.TelefonoType(CodigoPais=phone.country_code,
                                                      NumTelefono=phone.national_number))

        return sender

    def gen_receptor(self, classdoc):
        """Logica y validaciones del receptor de tipo de documento.

            :param object classdoc: Clase del tipo de documento.
            :returns: obj del comprador del tipo de documento electronico.
            """

        if not self.partner_id:
            return None

        voucher_type_code = self.voucher_type_code
        if voucher_type_code == '08' or self.invoice_type == 'in_refund':
            partner_id = self.company_id.partner_id
        else:
            partner_id = self.partner_id

        if not partner_id.country_id:
            raise ValidationError(_('Debe especificar el pais.'))
        if voucher_type_code in ['01', '08']:
            """Factura electrónica"""
            if not partner_id.identification_id:
                raise ValidationError(_('Debe especificar Tipo de identificacion.'))
            if not partner_id.vat:
                raise ValidationError(_('Debe especificar VAT.'))
            if partner_id.country_id == self.env.ref("base.cr"):
                if not partner_id.state_id:
                    raise ValidationError(_('The province of partner must be required.'))
                if partner_id.state_id:
                    if not partner_id.state_id.code:
                        raise ValidationError(
                            'La Provincia del cliente seleccionado no tiene codigo para Hacienda, favor corregir!')
                if not partner_id.canton_id:
                    raise ValidationError(_('Then canton of partner must be required.'))
                if partner_id.canton_id:
                    if not partner_id.canton_id.code:
                        raise ValidationError(
                            'El canton del cliente seleccionado no tiene codigo para Hacienda, favor corregir!')
                if not partner_id.distrito_id:
                    raise ValidationError(_('Then distrito of partner must be required.'))
                if partner_id.distrito_id:
                    if not partner_id.distrito_id.code:
                        raise ValidationError(
                            'El distrito del cliente seleccionado no tiene codigo para Hacienda, favor corregir!')

            if not partner_id.street:
                raise ValidationError(_('The buyer has not defined a street.'))

            receiver_name = self.limit(partner_id.name, 80)
            receiver = classdoc.ReceptorType(Nombre=receiver_name, Identificacion=None)
            receiver.set_Identificacion(classdoc.IdentificacionType(Tipo=partner_id.identification_id.code,
                                                                    Numero=partner_id.vat))
            if partner_id.commercial_name:
                receiver_commercial_name = partner_id.commercial_name.replace('&', ' ')
                receiver.set_NombreComercial(self.limit(receiver_commercial_name, 80))
            if partner_id.state_id and partner_id.canton_id and partner_id.distrito_id:
                location = classdoc.UbicacionType(Provincia=int(partner_id.state_id.code),
                                                  Canton=int(partner_id.canton_id.code),
                                                  Distrito=int(partner_id.distrito_id.code),
                                                  OtrasSenas=self.limit(partner_id.street, 250),
                                                  )
                if partner_id.neighborhood_id.name:
                    location.set_Barrio(self.limit(partner_id.neighborhood_id.name, 50))
                receiver.set_Ubicacion(location)
            if partner_id.phone or partner_id.mobile:
                tel = partner_id.phone if partner_id.phone else partner_id.mobile
                phone = phonenumbers.parse(tel, 'CR')
                receiver.set_Telefono(
                    classdoc.TelefonoType(CodigoPais=phone.country_code,
                                          NumTelefono=phone.national_number))
            if partner_id.email:
                receiver.set_CorreoElectronico(partner_id.email)

            return receiver
        elif voucher_type_code == '10':
            """Recibo Electrónico de Pago"""

            receiver_name = self.limit(partner_id.name, 80)
            receiver = classdoc.ReceptorType(Nombre=receiver_name, Identificacion=None)
            receiver.set_Identificacion(classdoc.IdentificacionType(Tipo=partner_id.identification_id.code,
                                                                    Numero=partner_id.vat))

            if partner_id.email:
                receiver.set_CorreoElectronico(partner_id.email)
            return receiver
        elif voucher_type_code == '09':
            """Factura electrónica de exportación"""

            if not partner_id.identification_id:
                raise ValidationError(_('Debe especificar Tipo de identificacion.'))
            if not partner_id.vat:
                raise ValidationError(_('Debe especificar VAT.'))
            receiver_name = self.limit(partner_id.name, 80)
            receiver = classdoc.ReceptorType(Nombre=receiver_name, Identificacion=None)
            if partner_id.email:
                receiver.set_CorreoElectronico(partner_id.email)

            return receiver
        elif voucher_type_code == '04':
            """TiqueteElectronico"""

            receiver_name = self.limit(partner_id.name, 80)
            receiver = classdoc.ReceptorType(Nombre=receiver_name, Identificacion=None)
            if partner_id.commercial_name:
                receptor_commercial_name = partner_id.commercial_name.replace('&', ' ')
                receiver.set_NombreComercial(self.limit(receptor_commercial_name, 80))
            identification = classdoc.IdentificacionType(Tipo=partner_id.identification_id.code,
                                                         Numero=partner_id.vat)
            if identification.get_Tipo() and identification.get_Numero():
                receiver.set_Identificacion(classdoc.IdentificacionType(Tipo=partner_id.identification_id.code,
                                                                        Numero=partner_id.vat))
            if partner_id.country_id == self.env.ref("base.cr"):
                if partner_id.state_id and partner_id.canton_id and partner_id.distrito_id:
                    location = classdoc.UbicacionType(Provincia=int(partner_id.state_id.code),
                                                      Canton=int(partner_id.canton_id.code),
                                                      Distrito=int(partner_id.distrito_id.code))
                    if partner_id.neighborhood_id.name:
                        location.set_Barrio(self.limit(partner_id.neighborhood_id.name, 50))

                    location.set_OtrasSenas(self.limit(partner_id.street or "NA", 250))
                    receiver.set_Ubicacion(location)
            else:
                receiver.set_OtrasSenasExtranjero(partner_id.street or "NAAAAA")
            if partner_id.phone or partner_id.mobile:
                tel = partner_id.phone if partner_id.phone else partner_id.mobile
                phone = phonenumbers.parse(tel, 'CR')
                receiver.set_Telefono(
                    classdoc.TelefonoType(CodigoPais=phone.country_code,
                                          NumTelefono=phone.national_number))
            if partner_id.email:
                receiver.set_CorreoElectronico(partner_id.email)

            return receiver
        else:
            """ NC y ND"""

            # if not partner_id.identification_id:
            #     raise ValidationError(_('Debe especificar Tipo de identificacion.'))
            # if not partner_id.vat:
            #     raise ValidationError(_('Debe especificar VAT.'))

            receiver_name = self.limit(partner_id.name, 80)
            receiver = classdoc.ReceptorType(Nombre=receiver_name, Identificacion=None)
            if partner_id.commercial_name:
                receptor_commercial_name = partner_id.commercial_name.replace('&', ' ')
                receiver.set_NombreComercial(self.limit(receptor_commercial_name, 80))
            if partner_id.country_id == self.env.ref("base.cr"):
                identification = classdoc.IdentificacionType(Tipo=partner_id.identification_id.code,
                                                             Numero=partner_id.vat)
                if identification.get_Tipo() and identification.get_Numero():
                    receiver.set_Identificacion(classdoc.IdentificacionType(Tipo=partner_id.identification_id.code,
                                                                            Numero=partner_id.vat))
                if partner_id.state_id and partner_id.canton_id and partner_id.distrito_id:
                    location = classdoc.UbicacionType(Provincia=int(partner_id.state_id.code),
                                                      Canton=int(partner_id.canton_id.code),
                                                      Distrito=int(partner_id.distrito_id.code))
                    if partner_id.neighborhood_id.name:
                        location.set_Barrio(self.limit(partner_id.neighborhood_id.name, 50))
                    location.set_OtrasSenas(self.limit(partner_id.street or "NA", 250))
                    receiver.set_Ubicacion(location)
            else:
                receiver.set_OtrasSenasExtranjero(partner_id.street or "NAAAAA")
            if partner_id.phone or partner_id.mobile:
                tel = partner_id.phone if partner_id.phone else partner_id.mobile
                phone = phonenumbers.parse(tel, 'CR')
                receiver.set_Telefono(
                    classdoc.TelefonoType(CodigoPais=phone.country_code,
                                          NumTelefono=phone.national_number))
            if partner_id.email:
                receiver.set_CorreoElectronico(partner_id.email)

            return receiver

    def _get_other_charges(self, classdoc):
        """ Otros cargos que forman parte del costo total de la línea de detalle.

            :param object classdoc: Clase del tipo de documento.
            :returns: list
            """

        other_charges = []
        if self.invoice_id:
            lines = self.invoice_id.invoice_line_ids
        else:
            if 'order_id' in self._fields:
                order_id = self.order_id
                lines = order_id.lines

        for i, line in enumerate(self._iterable_products_xml(lines),  1):
            display_type = False
            if self.invoice_id:
                if line.display_type != 'product':
                    display_type = True

            if not display_type:
                if self.invoice_id:
                    taxes = line.tax_ids
                else:
                    taxes = line.tax_ids_after_fiscal_position

                for t in taxes.filtered(lambda l: l.tax_group_id.l10n_cr_billing_indicator):
                    charges = {"document_type": t.tax_group_id.l10n_cr_billing_indicator,
                               "charge_amount": abs(line.price_subtotal * (t.amount / 100)),
                               "percent": t.amount,
                               "detail": t.name}
                    other_charges.append(charges)

        # Usamos defaultdict para agrupar los cargos por tipo de documento y porcentaje
        group_charge_info = defaultdict(lambda: {"detail": "", "charge_amount": 0})
        for item in other_charges:
            clave = (item["document_type"], item["percent"])
            group_charge_info[clave]["detail"] = item["detail"]
            group_charge_info[clave]["charge_amount"] += item["charge_amount"]

        result_charge = [
            {"document_type": k[0], "percent": k[1], "detail": v["detail"], "charge_amount": v["charge_amount"]}
            for k, v in group_charge_info.items()
        ]

        other_charges_obj = []
        for r in result_charge:
            charges = classdoc.OtrosCargosType(TipoDocumentoOC=r["document_type"],
                                               MontoCargo=r["charge_amount"],
                                               PorcentajeOC=r["percent"],
                                               Detalle=r["detail"],
                                               )
            other_charges_obj.append(charges)

        return other_charges_obj

    def _iterable_products_xml(self, lines):
        self.ensure_one()
        return lines

    def _get_item_total_vals(self, cedoc, detailed_type, indicator_prod_service):
        """
        :param cedoc: .
        :param detailed_type: Mercancias o bienes.
        :return: {
            'total_exempt': 0.0,    # Total exento
            'total_exonerado': 0.0,    # Total exonerado
            'total_taxable': 0.0,    # Total grabado con IVA
        }
        """
        dict_total = {}
        totals_taxable_vals = defaultdict(int)
        totals_exoneration_vals = defaultdict(int)
        totals_exempt_vals = defaultdict(int)
        totals_not_subject_vals = defaultdict(int)
        detail_lines = cedoc.get_DetalleServicio().get_LineaDetalle()
        for line in detail_lines:
            tax_list = list(filter(lambda t: t.indicator_prod_service == indicator_prod_service, line.get_Impuesto()))
            for tax in tax_list:
                tax_code = tax.get_Codigo()
                iva_tax_rate_code = tax.get_CodigoTarifaIVA()
                tax_iva_id = self.env["account.tax"].search([('code_cr', '=', tax_code),
                                                             ('iva_tax_rate', '=', iva_tax_rate_code),
                                                             ('tax_scope', 'in', detailed_type),
                                                             ('company_id', 'parent_of', self.company_id.ids),
                                                             ('country_id', '=', self.env.ref("base.cr").id)
                                                             ], limit=1)
                if tax.NoSujeto:
                    totals_not_subject_vals[tax_iva_id.id] += line.get_MontoTotal()
                elif tax_iva_id:
                    if self.voucher_type_code in ["09", "10"]:
                        if iva_tax_rate_code in ['01', '10']:
                            totals_exempt_vals[tax_iva_id.id] += line.get_MontoTotal()
                        else:
                            totals_taxable_vals[tax_iva_id.id] += line.get_MontoTotal()
                    elif tax.get_Exoneracion():
                        exoneration = tax.get_Exoneracion()
                        amount_taxable = tax.Monto - exoneration.MontoExoneracion
                        if amount_taxable == 0.0:
                            totals_exoneration_vals[tax_iva_id.id] += line.get_MontoTotal()
                        else:
                            if iva_tax_rate_code in ['01', '10']:
                                totals_exempt_vals[tax_iva_id.id] += line.get_MontoTotal()
                            else:
                                totals_taxable_vals[tax_iva_id.id] += line.get_MontoTotal()
                        #
                        #
                        # #aa = ((tax.get_Tarifa() - tax.get_Exoneracion().get_TarifaExonerada()) / 100)
                        # #bb = tax.get_Tarifa() / 100
                        # #cc = aa / bb
                        # #MontoTotal = line.get_MontoTotal()
                        # #totals_taxable_vals[tax_iva_id.id] += line.get_MontoTotal() * cc
                        # #totals_exoneration_vals[tax_iva_id.id] += line.get_MontoTotal() - (line.get_MontoTotal() * cc)
                        # exoneration = tax.get_Exoneracion()
                        # #totals_exoneration_vals[tax_iva_id.id] += exoneration.MontoExoneracion
                        # #amount_taxable = tax.Monto - exoneration.MontoExoneracion
                        # amount_taxable = tax.Monto - exoneration.MontoExoneracion
                        # if amount_taxable == 0.0:
                        #     totals_exoneration_vals[tax_iva_id.id] += line.get_MontoTotal()
                    else:
                        if iva_tax_rate_code in ['01', '10']:
                            totals_exempt_vals[tax_iva_id.id] += line.get_MontoTotal()
                        else:
                            totals_taxable_vals[tax_iva_id.id] += line.get_MontoTotal()

            # if not tax_list and indicator_prod_service == 1:
            #     # Se establece Mercaderia por omision de impuesto.
            #     totals_exempt_vals[line.get_MontoTotal()] += line.get_MontoTotal()

            # if not tax_list and indicator_prod_service == line.indicator_prod_service:
            #     totals_exempt_vals[line.get_MontoTotal()] += line.get_MontoTotal()

        total_taxable = sum([v for k, v in totals_taxable_vals.items()])
        dict_total["total_taxable"] = total_taxable
        total_exempt = sum([v for k, v in totals_exempt_vals.items()])
        dict_total["total_exempt"] = total_exempt
        total_exoneration = sum([v for k, v in totals_exoneration_vals.items()])
        dict_total["total_exonerado"] = total_exoneration
        total_not_subject = sum([v for k, v in totals_not_subject_vals.items()])
        dict_total["total_no_subject"] = total_not_subject
        return dict_total

    def _construct_tax_excluded(self, price, line):
        res = line.tax_ids.compute_all(price, product=line.product_id, partner=self.env['res.partner'])
        excluded = res['total_excluded']
        return excluded

    def _gen_detail_and_summary(self, cedoc, classdoc):
        """Detalle y Resumen

            :param object cedoc: Instancia del Elemento raiz.
            :param object classdoc: Clase del tipo de documento.
            :param char reference_nc: Origen.

            :returns: object cedoc
            """

        condition_sale = cedoc.get_CondicionVenta()
        if condition_sale != '01':  # es a credito u otros
            mayor = 1
            for pline in self.invoice_id.invoice_payment_term_id.line_ids:
                if pline.nb_days > mayor:
                    mayor = pline.nb_days
            cedoc.set_PlazoCredito(mayor)

        detail = classdoc.DetalleServicioType()
        currency = self.currency_id
        total_discount = 0.0
        if self.invoice_id:
            lines = self.invoice_id.invoice_line_ids
            _date = self.invoice_id.invoice_date
        else:
            if 'order_id' in self._fields:
                order_id = self.order_id
                lines = order_id.lines
                _date = self.order_id.date_order

        exoneration = False
        if (self.invoice_id.partner_id.l10n_cr_exoneration_authorization
                and self.voucher_type_id.code != '09'):
            exoneration = True

        tax_data = self.get_taxed_amount_data(lines)
        total_iva = sum(
            [
                tax_data["02_taxed_amount"],
                tax_data["03_taxed_amount"],
                tax_data["04_taxed_amount"],
                tax_data["05_taxed_amount"],
                tax_data["06_taxed_amount"],
                tax_data["07_taxed_amount"],
                tax_data["08_taxed_amount"],
                tax_data["09_taxed_amount"],
                tax_data["10_taxed_amount"],
            ]
        )

        total_taxed_service = 0.00
        total_exempt_service = 0.00
        total_taxed_product = 0.00
        total_exempt_product = 0.00
        total_product_exonerated = 0.00
        total_service_exonerated = 0.00
        total_product_not_subject = 0.00
        total_service_not_subject = 0.00
        base_subtotal = 0.0
        for i, line in enumerate(self._iterable_products_xml(lines),  1):
            discount_amount = 0.0
            display_type = False
            if self.invoice_id:
                if line.display_type != 'product':
                    display_type = True

            if not display_type:
                total_impuestos = 0.0
                product_id = line.product_id
                if self.invoice_id:
                    quantity = line.quantity
                    taxes = line.tax_ids
                else:
                    quantity = line.qty
                    taxes = line.tax_ids_after_fiscal_position

                if not all([tax.code_cr for tax in taxes]):
                    raise ValidationError(
                        'Por favor configure los campos código y tarifa para los impuesto.'
                    )
                if self.voucher_type_code != "10" and not product_id.product_cabys_id:
                    if self.voucher_type_code in ["02", "03"] and self.invoice_id and self.invoice_id.cod_referencia_id.code not in ["09", "09"]:
                        raise ValidationError(
                            f"El producto {product_id.name} carece de Codigo CABYS, no se puede generar XML. Origen: {self.get_origin_name()}")
                    raise ValidationError(
                        f"El producto {product_id.name} carece de Codigo CABYS, no se puede generar XML. Origen: {self.get_origin_name()}")

                # if product_id.product_cabys_id and len(product_id.product_cabys_id.code) < 13:
                #     raise UserError(
                #         f"El codigo CABYS {product_id.product_cabys_id.code} del producto {product_id.name} debe tener minimo 13 digitos para poder ser aceptado por Hacienda, "
                #         "de lo contrario sera rechazado incluso existiendo códigos de 12 dígitos correctos.")

                price_unit_untaxed = self._construct_tax_excluded(line.price_unit, line)
                item = classdoc.LineaDetalleType(
                    NumeroLinea=i,
                    Cantidad=abs(quantity),
                    PrecioUnitario=abs(price_unit_untaxed),
                )
                if self.voucher_type_code in ["01", "04"]:
                    item.set_ImpuestoAsumidoEmisorFabrica(0.00)
                if self.voucher_type_code not in ["10"] and product_id.product_cabys_id.code != '0000000000000':
                    item.set_CodigoCABYS(product_id.product_cabys_id.code)
                self.set_item_additional_vals(line, item, cedoc, classdoc)
                if self.voucher_type_code not in ["08", "10"] and product_id.type == 'combo' and product_id.combo_ids:
                    surtido_detail = self._gen_surtido_detail(line, item, cedoc, classdoc)
                    item.set_DetalleSurtido(surtido_detail)
                if self.voucher_type_code == "09":
                    if product_id.l10n_sv_tariff_item and len(product_id.l10n_sv_tariff_item) < 12:
                        raise UserError(
                            "Partida arancelaria del producto %s debe tener 12 digitos. Digitos actuales: %s" % (
                                product_id.name, len(product_id.l10n_sv_tariff_item)))

                if self.voucher_type_code == '09' and product_id.l10n_sv_tariff_item:
                    item.set_PartidaArancelaria(self.limit(product_id.l10n_sv_tariff_item, 12))
                if product_id.barcode:
                    item.add_CodigoComercial(
                        classdoc.CodigoType(Tipo='03', Codigo=self.limit(product_id.barcode, 20)))
                if product_id.default_code:
                    item.add_CodigoComercial(
                        classdoc.CodigoType(Tipo='04', Codigo=self.limit(product_id.default_code, 20)))
                if line.product_uom_id:
                    if not line.product_uom_id.code:
                        raise ValidationError('La unidad de medida no tiene codigo para Hacienda.')
                    item.set_UnidadMedida(line.product_uom_id.code)
                    item.set_UnidadMedidaComercial(self.limit(line.product_uom_id.name, 20))
                else:
                    item.set_UnidadMedida('Unid')
                if self.invoice_id:
                    line_name = line.name or line.product_id.name
                else:
                    if 'order_id' in self._fields:
                        line_name = line.full_product_name
                item.set_Detalle(self.limit(line_name, 160))
                price_unit = round(price_unit_untaxed, 5)
                base_line = abs(round(price_unit * quantity, 5))
                item.set_MontoTotal(base_line)
                if self.invoice_id:
                    discount_type_code = line.l10n_cr_discount_type_code or "07"
                else:
                    discount_type_code = "07"
                if line.discount > 0:
                    discount_amount = price_unit * quantity * line.discount / 100
                    total_discount += discount_amount
                    discount = classdoc.DescuentoType(MontoDescuento=discount_amount,
                                                      CodigoDescuento=discount_type_code,
                                                      NaturalezaDescuento=L10N_CR_DESCRIPTION_DISCOUNT_TYPE_CODE_MAP[discount_type_code])
                    item.add_Descuento(discount)
                subtotal_line = base_line - discount_amount
                base_subtotal += subtotal_line
                item.set_SubTotal(abs(subtotal_line))
                if self.voucher_type_code in ["01", "02", "03", "04", "08"]:
                    item.set_BaseImponible(item.get_SubTotal())
                impuesto_neto = 0.0
                # Only taxes with codes IVA.
                tax_ids = taxes.filtered(lambda l: l.iva_tax_rate in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"] and not l.is_exonerated)
                for t in tax_ids:
                    imp = t
                    if exoneration and self.invoice_id.fiscal_position_id:
                        for tax_map in self.invoice_id.fiscal_position_id.tax_ids:
                            if tax_map.tax_dest_id.id == t.id and \
                                    tax_map.tax_src_id.id in line.product_id.taxes_id.ids:
                                imp = tax_map.tax_src_id
                    impuesto = classdoc.ImpuestoType(Codigo=imp.code_cr, Tarifa=imp.amount,
                                                     indicator_prod_service=2 if imp.tax_scope == 'service' else 1)
                    if imp.code_cr in ['01', '07']:
                        "Se convierte en obligatorio para los Códigos 01, 07."
                        impuesto.set_CodigoTarifaIVA(imp.iva_tax_rate or '08')
                    if exoneration:
                        fpos = self.invoice_id.fiscal_position_id
                        if not self.partner_id.l10n_cr_institution_name:
                            raise UserError(_('El cliente debe tener un nombre de institución para la exoneración.'))

                        for tax_map in fpos.tax_ids:
                            if tax_map.tax_dest_id.id == t.id and tax_map.tax_src_id.id == imp.id:
                                purchase_amount = int(imp.amount - t.amount)
                                porcentaje_exoneracion_calculo = float(purchase_amount) / 100
                                monto_exoneracion = line.price_subtotal * porcentaje_exoneracion_calculo
                                exoneration = classdoc.ExoneracionType(TipoDocumento=self.partner_id.l10n_cr_document_type_id.ce_code,
                                                                       NumeroDocumento=self.partner_id.l10n_cr_document_number,
                                                                       NombreInstitucion=self.partner_id.l10n_cr_institution_name,
                                                                       FechaEmision=self.partner_id.l10n_cr_issue_date,
                                                                       TarifaExonerada=purchase_amount,
                                                                       MontoExoneracion=monto_exoneracion,
                                                                       )
                                impuesto.set_Exoneracion(exoneration)
                                break

                        tax_exonerated = taxes.filtered(lambda tax: tax.id != t.id and tax.is_exonerated)
                        for te in tax_exonerated:
                            porcentaje_exoneracion_calculo = float(abs(te.amount)) / 100
                            monto_exoneracion = line.price_subtotal * porcentaje_exoneracion_calculo
                            exoneration = classdoc.ExoneracionType(
                                TipoDocumento=self.partner_id.l10n_cr_document_type_id.ce_code,
                                NumeroDocumento=self.partner_id.l10n_cr_document_number,
                                NombreInstitucion=self.partner_id.l10n_cr_institution_name,
                                FechaEmision=self.partner_id.l10n_cr_issue_date,
                                TarifaExonerada=self.partner_id.l10n_cr_percentage_exoneration,
                                MontoExoneracion=monto_exoneracion,
                                #TarifaExonerada=purchase_amount,
                                #MontoExoneracion=monto_exoneracion,
                                )
                            impuesto.set_Exoneracion(exoneration)
                            break





                    monto_impuesto = float(subtotal_line * imp.amount) / 100
                    impuesto.set_Monto(abs(monto_impuesto))
                    if self.voucher_type_id.code not in ['09', '10']:
                        impuesto_neto += (0
                                          # if line.l10n_cr_has_exoneration and self.invoice_id.exoneration_id.purchase_amount == 100.00
                                          if self.invoice_id
                                             and line.l10n_cr_has_exoneration
                                             and self.partner_id.l10n_cr_percentage_exoneration == 100.00
                                          else (
                                              impuesto.get_Monto()
                                              if not impuesto.get_Exoneracion()
                                              else
                                              impuesto.get_Monto() - impuesto.get_Exoneracion().get_MontoExoneracion()
                                          ))
                    else:
                        impuesto_neto = impuesto.get_Monto()

                    # if imp.amount:
                    #     item.add_Impuesto(impuesto)

                    item.add_Impuesto(impuesto)

                # Taxes exempt by omission.
                if not taxes:
                    no_subject = True
                    #MACK
                    indicator = 1
                    if line.product_id and line.product_id.type and line.product_id.type in ['service', 'consu']:
                        indicator = 1
                    else:
                        indicator = 2
                    impuesto = classdoc.ImpuestoType(Codigo='01',
                                                     Tarifa=0.00,
                                                     CodigoTarifaIVA='01',
                                                     Monto=0.00,
                                                     indicator_prod_service=indicator,
                                                     NoSujeto=True
                                                     )
                    item.add_Impuesto(impuesto)
                # if not taxes :
                #     pass

                monto_total_linea = impuesto_neto + abs(subtotal_line)
                total_impuestos += impuesto_neto
                if self.voucher_type_id.code != '09':
                    item.set_ImpuestoNeto(abs(impuesto_neto))
                item.set_MontoTotalLinea(abs(monto_total_linea))
                detail.add_LineaDetalle(item)
        if total_product_exonerated == total_exempt_product:
            total_product_exonerated = 0
        if total_service_exonerated == total_exempt_service:
            total_service_exonerated = 0
        cedoc.set_DetalleServicio(detail)
        total_product = self._get_item_total_vals(cedoc, ['consu'], indicator_prod_service=1)  # 1: product
        total_service = self._get_item_total_vals(cedoc, ['service'], indicator_prod_service=2)  # 2: service
        totals_vals = {"TotalServ": total_service,
                       "TotalMercancias": total_product}
        if totals_vals["TotalServ"]:
            total_taxed_service = totals_vals["TotalServ"]['total_taxable']
            total_exempt_service = totals_vals["TotalServ"]['total_exempt']
            total_service_exonerated = totals_vals["TotalServ"]['total_exonerado']
            total_service_not_subject = totals_vals["TotalServ"]['total_no_subject']
        if totals_vals["TotalMercancias"]:
            total_taxed_product = totals_vals["TotalMercancias"]['total_taxable']
            total_exempt_product = totals_vals["TotalMercancias"]['total_exempt']
            total_product_exonerated = totals_vals["TotalMercancias"]['total_exonerado']
            total_product_not_subject = totals_vals["TotalMercancias"]['total_no_subject']

        summary = classdoc.ResumenFacturaType(TotalComprobante=0.00, CodigoTipoMoneda=None)
        if self.invoice_id:
            code_currency_type = classdoc.CodigoMonedaType(CodigoMoneda=self.invoice_id.currency_id.name)
            rate = self.invoice_id.currency_rate
            code_currency_type.set_TipoCambio(abs(rate))
        elif 'order_id' in self._fields:
            code_currency_type = classdoc.CodigoMonedaType(CodigoMoneda=self.order_id.currency_id.name)
            date = _date
            rate = currency.with_context(dict(self._context or {}, date=date)).rate
            rate = round(1.0 / rate, 5)
            code_currency_type.set_TipoCambio(abs(rate))
        summary.set_CodigoTipoMoneda(code_currency_type)
        summary.set_TotalServGravados(abs(total_taxed_service))
        if self.voucher_type_id.code != '09' and total_service_exonerated > 0.0:
            summary.set_TotalServExonerado(total_service_exonerated)
        summary.set_TotalServExentos(abs(total_exempt_service))
        summary.set_TotalMercanciasGravadas(abs(total_taxed_product))
        summary.set_TotalMercanciasExentas(abs(total_exempt_product))
        summary.set_TotalMercNoSujeta(abs(total_product_not_subject)) #MACK
        summary.set_TotalServNoSujeto(abs(total_service_not_subject)) #MACK
        if self.voucher_type_id.code != '09' and total_product_exonerated > 0.0:
            summary.set_TotalMercExonerada(total_product_exonerated)
        total_taxed = total_taxed_service + total_taxed_product
        summary.set_TotalGravado(round(abs(total_taxed), 5))
        summary.set_TotalExento(summary.get_TotalMercanciasExentas() + summary.get_TotalServExentos())
        if self.voucher_type_id.code not in ['09', '10']:
            summary.set_TotalExonerado(round(abs(total_service_exonerated + total_product_exonerated), 5))
        if self.voucher_type_id.code not in ['09', '10']:
            total_sale = float(summary.get_TotalGravado()) + float(summary.get_TotalExento()) + float(summary.get_TotalExonerado())
            #total_sale = float(summary.get_TotalGravado()) + float(summary.get_TotalExento())
        else:
            total_sale = float(summary.get_TotalGravado()) + float(summary.get_TotalExento())
        if total_discount > 0.0:
            summary.set_TotalDescuentos(total_discount)
        total_no_sujeto = float(summary.get_TotalServNoSujeto()) + float(summary.get_TotalMercNoSujeta())# MACK
        summary.set_TotalNoSujeto(abs(total_no_sujeto))# MACK
        total_sale += total_no_sujeto# MACK
        summary.set_TotalVenta(abs(total_sale))
        tax_breakdown_data = self.get_desglose_impuesto_data(cedoc, classdoc)
        for impuesto_data in tax_breakdown_data.values():
            total_desglose_impuesto = classdoc.TotalDesgloseImpuesto(Codigo=impuesto_data['tax_code'],
                                                                     CodigoTarifaIVA=impuesto_data.get('iva_tax_rate_code', None),
                                                                     TotalMontoImpuesto=impuesto_data['amount_total'])
            summary.add_TotalDesgloseImpuesto(total_desglose_impuesto)
        summary.set_TotalVentaNeta(float(summary.get_TotalVenta()) - float(summary.get_TotalDescuentos()))
        summary.set_TotalImpuesto(abs(total_iva))
        if cedoc.get_OtrosCargos():
            total_other_charges = sum([other.get_MontoCargo() for other in cedoc.get_OtrosCargos()])
            summary.set_TotalOtrosCargos(total_other_charges)
        if self.payment_term_type_id.code not in ['02', '08', '10']:
            # Para condición de la venta correspondientes a créditos no aplican medios de pagos.
            summary.set_MedioPago(self.get_payment_way(cedoc, classdoc))
        summary.set_TotalComprobante(
            abs(summary.get_TotalVentaNeta() + summary.get_TotalImpuesto() + summary.get_TotalOtrosCargos()))
        cedoc.set_ResumenFactura(summary)
        return cedoc

    def _gen_surtido_detail(self, line, item, cedoc, classdoc):
        detail_surtido = classdoc.DetalleSurtido()
        for combo in line.product_id.combo_ids:
            for combo_item in combo.combo_item_ids:
                item = classdoc.LineaDetalleSurtido(
                    CodigoCABYSSurtido=combo_item.product_id.product_cabys_id.code,
                    CantidadSurtido=1,
                    UnidadMedidaSurtido=combo_item.product_id.product_tmpl_id.uom_id.code,
                    DetalleSurtido=combo_item.product_id.name,
                    PrecioUnitarioSurtido=combo_item.lst_price,
                )
                item.set_MontoTotalSurtido(item.get_CantidadSurtido() * item.get_PrecioUnitarioSurtido())
                item.set_SubTotalSurtido(item.get_MontoTotalSurtido())
                item.set_BaseImponibleSurtido(item.get_MontoTotalSurtido())
                impuesto_surtido = classdoc.ImpuestoSurtido(CodigoImpuestoSurtido="01",
                                                            CodigoTarifaIVASurtido="08",
                                                            TarifaSurtido=13.0,
                                                            MontoImpuestoSurtido=item.get_BaseImponibleSurtido() * 0.13,
                                                            )
                item.add_ImpuestoSurtido(impuesto_surtido)
                detail_surtido.add_LineaDetalleSurtido(item)

        return detail_surtido

    def get_desglose_impuesto_data(self, cedoc=None, classdoc=None):
        """Obtiene el resumen impuestos por lineas de detalle.

        :return: {
            'tax_code': '01',    # Codigo
            'iva_tax_rate_code': '08',    # CodigoTarifaIVA
            'amount_total'    : 130.0,    # TotalMontoImpuesto
        }
        """

        tax_total_values = {}
        detail_lines = cedoc.get_DetalleServicio().get_LineaDetalle()
        for line in detail_lines:
            for tax in line.get_Impuesto():
                tax_code = tax.get_Codigo()
                iva_tax_rate_code = tax.get_CodigoTarifaIVA()
                amount_total = tax.get_Monto()
                tax_iva_id = self.env["account.tax"].search([('code_cr', '=', tax_code),
                                                             ('iva_tax_rate', '=', iva_tax_rate_code),
                                                             ('company_id', 'parent_of', self.company_id.ids),
                                                             ('country_id', '=', self.env.ref("base.cr").id)
                                                             ], limit=1)
                if self.voucher_type_code in ["09", "10"]:
                    if tax_iva_id.id not in tax_total_values:
                        tax_total_values[tax_iva_id.id] = {
                            'tax_code': tax_code,
                            'iva_tax_rate_code': iva_tax_rate_code,
                            'amount_total': amount_total,
                        }
                    else:
                        tax_total_values[tax_iva_id.id]['amount_total'] += amount_total
                elif not tax.get_Exoneracion():
                    if tax_iva_id.id not in tax_total_values:
                        tax_total_values[tax_iva_id.id] = {
                            'tax_code': tax_code,
                            'iva_tax_rate_code': iva_tax_rate_code,
                            'amount_total': amount_total,
                        }
                    else:
                        tax_total_values[tax_iva_id.id]['amount_total'] += amount_total
                else:
                    if tax_iva_id.id not in tax_total_values:
                        tax_total_values[tax_iva_id.id] = {
                            'tax_code': tax_code,
                            'iva_tax_rate_code': iva_tax_rate_code,
                            'amount_total': line.get_ImpuestoNeto(),
                        }
                    else:
                        tax_total_values[tax_iva_id.id]['amount_total'] += line.get_ImpuestoNeto()

        return tax_total_values

    def _gen_detail_and_summary_rep(self, cedoc, classdoc):
        """Detalle y Resumen

            :param object cedoc: Instancia del Elemento raiz.
            :param object classdoc: Clase del tipo de documento.
            :param char reference_nc: Origen.

            :returns: object cedoc
            """

        detail = classdoc.DetalleServicioType()
        # currency = self.currency_id
        # total_discount = 0.0

        if self.invoice_id:
            lines = self.invoice_id.invoice_line_ids
            _date = self.invoice_id.invoice_date

        tax_data = self.get_taxed_amount_data(lines)
        total_iva = sum(
            [
                tax_data["02_taxed_amount"],
                tax_data["03_taxed_amount"],
                tax_data["04_taxed_amount"],
                tax_data["05_taxed_amount"],
                tax_data["06_taxed_amount"],
                tax_data["07_taxed_amount"],
                tax_data["08_taxed_amount"],
                tax_data["09_taxed_amount"],
                tax_data["10_taxed_amount"],
            ]
        )
        base_subtotal = 0.0
        for i, line in enumerate(self._iterable_products_xml(lines),  1):
            discount_amount = 0.0
            display_type = False
            if self.invoice_id:
                if line.display_type != 'product':
                    display_type = True

            if not display_type:
                total_impuestos = 0.0
                product_id = line.product_id
                if self.invoice_id:
                    quantity = line.quantity
                    taxes = line.tax_ids
                else:
                    quantity = line.qty
                    taxes = line.tax_ids_after_fiscal_position
                if not all([tax.code_cr for tax in taxes]):
                    raise ValidationError(
                        'Por favor configure los campos código y tarifa para los impuesto.'
                    )
                price_unit_untaxed = self._construct_tax_excluded(line.price_unit, line)
                item = classdoc.LineaDetalleType(
                    NumeroLinea=i,
                )
                if self.voucher_type_code in ["01", "04"]:
                    item.set_ImpuestoAsumidoEmisorFabrica(0.00)
                self.set_item_additional_vals(line, item, cedoc, classdoc)
                if self.invoice_id:
                    line_name = line.name or line.product_id.name
                item.set_Detalle(self.limit(line_name, 160))
                price_unit = round(price_unit_untaxed, 5)
                base_line = abs(round(price_unit * quantity, 5))
                item.set_MontoTotal(base_line)
                subtotal_line = base_line - discount_amount
                base_subtotal += subtotal_line
                item.set_SubTotal(abs(subtotal_line))
                if self.voucher_type_code in ["01", "02", "03", "04", "08"]:
                    item.set_BaseImponible(item.get_SubTotal())
                impuesto_neto = 0.0
                # Only taxes with codes IVA.
                for t in taxes.filtered(
                        lambda l: l.iva_tax_rate in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]):
                    imp = t
                    impuesto = classdoc.ImpuestoType(Codigo=imp.code_cr, Tarifa=imp.amount,
                                                     indicator_prod_service=2 if imp.tax_scope == 'service' else 1)
                    if imp.code_cr in ['01', '07']:
                        "Se convierte en obligatorio para los Códigos 01, 07."
                        impuesto.set_CodigoTarifaIVA(imp.iva_tax_rate or '08')

                    monto_impuesto = float(subtotal_line * imp.amount) / 100
                    impuesto.set_Monto(abs(monto_impuesto))
                    if self.voucher_type_id.code not in ['09', '10']:
                        impuesto_neto += (0
                                          if self.invoice_id
                                             and line.l10n_cr_has_exoneration
                                             and self.partner_id.l10n_cr_percentage_exoneration == 100.00
                                          else (
                                              impuesto.get_Monto()
                                              if not impuesto.get_Exoneracion()
                                              else
                                              impuesto.get_Monto() - impuesto.get_Exoneracion().get_MontoExoneracion()
                                          ))
                    else:
                        impuesto_neto = impuesto.get_Monto()

                    item.add_Impuesto(impuesto)

                # Taxes exempt by omission.
                if not taxes and product_id.detailed_type:
                    impuesto = classdoc.ImpuestoType(Codigo='01',
                                                     Tarifa=0.00,
                                                     CodigoTarifaIVA='01',
                                                     Monto=0.00,
                                                     indicator_prod_service=2 if imp.tax_scope == 'service' else 1
                                                     )
                    item.add_Impuesto(impuesto)
                monto_total_linea = impuesto_neto + abs(subtotal_line)
                total_impuestos += impuesto_neto
                if self.voucher_type_id.code != '09':
                    item.set_ImpuestoNeto(abs(impuesto_neto))
                item.set_MontoTotalLinea(abs(monto_total_linea))
                detail.add_LineaDetalle(item)
        cedoc.set_DetalleServicio(detail)
        summary = classdoc.ResumenFacturaType(TotalComprobante=0.00, CodigoTipoMoneda=None)
        if self.invoice_id:
            code_currency_type = classdoc.CodigoMonedaType(CodigoMoneda=self.invoice_id.currency_id.name)
            rate = self.invoice_id.currency_rate
            code_currency_type.set_TipoCambio(abs(rate))
        summary.set_CodigoTipoMoneda(code_currency_type)
        summary.set_TotalVenta(abs(self.invoice_id.amount_untaxed))
        tax_breakdown_data = self.get_desglose_impuesto_data(cedoc, classdoc)
        for impuesto_data in tax_breakdown_data.values():
            total_desglose_impuesto = classdoc.TotalDesgloseImpuesto(Codigo=impuesto_data['tax_code'],
                                                                     CodigoTarifaIVA=impuesto_data.get('iva_tax_rate_code', None),
                                                                     TotalMontoImpuesto=impuesto_data['amount_total'])
            summary.add_TotalDesgloseImpuesto(total_desglose_impuesto)
        summary.set_TotalVentaNeta(float(summary.get_TotalVenta()))
        summary.set_TotalImpuesto(abs(total_iva))
        summary.set_MedioPago(self.get_payment_way(cedoc, classdoc))
        summary.set_TotalComprobante(
            abs(summary.get_TotalVentaNeta() + summary.get_TotalImpuesto()))
        cedoc.set_ResumenFactura(summary)
        return cedoc

    def get_payment_way(self, cedoc=None, classdoc=None):
        """ Medios de pagos usados.

                :param object classdoc: Clase del tipo de documento.
                :returns: list
                """

        payment_methods = []
        if self.invoice_id:
            payment_method_id = self.invoice_id.l10n_cr_payment_method_id
            if payment_method_id:
                payment_methods.append(classdoc.MedioPago(TipoMedioPago=payment_method_id.code,
                                                          TotalMedioPago=abs(self.xml_amount_total)))
            else:
                payment_methods.append(classdoc.MedioPago(TipoMedioPago="01", TotalMedioPago=abs(self.xml_amount_total)))

        return payment_methods

    def set_item_additional_vals(self, line, item, *args):
        """Set additional values to the item.
        """
        pass

    def set_additional_vals(self, cedoc, classdoc, *args):
        """Set additional values to the item.
        """
        pass

    # def set_summary_additional_vals(self, *args):
    #     """Set additional values to the summary.
    #     """
    #     pass

    def _add_reference_information(self, cedoc, classdoc, reference_nc):
        """Informacion Referencia

                :param object cedoc: Instancia del Elemento raiz.
                :param object classdoc: Clase del tipo de documento.
                :param char reference_nc: Origen.

                :returns: object cedoc
                """

        info_reference = classdoc.InformacionReferenciaType()
        if self.voucher_type_code in ['02', '03']:
            if self.invoice_id:
                info_reference.set_TipoDoc(self.invoice_id.cod_doc_ref or "04")
            if self.invoice_id and self.invoice_id.cod_doc_ref != '13':
                if self.voucher_type_code == '02':
                    key_numeric_ref = self.invoice_id.debit_origin_id.document_id.name
                elif self.voucher_type_code == '03':
                    key_numeric_ref = self.invoice_id.numero_ref or reference_nc
                else:
                    key_numeric_ref = "%s%s%s%s" % (
                        self.terminal_id.location_id.code,
                        self.terminal_id.code,
                        self.invoice_id.cod_doc_ref,
                        str(self.invoice_id.numero_ref).zfill(10))
                    key_numeric_ref = self.invoice_id.gen_key_numeric(key_numeric_ref)
                if not key_numeric_ref:
                    raise UserError(_("There is not Clave numerica to modifier."))
                info_reference.set_Numero(key_numeric_ref)

            if self.invoice_id.cod_doc_ref == '08':
                date_issue = self.date_issue_ref
            else:
                date_issue = self.get_time_now_cr()
            info_reference.set_FechaEmision(date_issue)
            if self.invoice_id and self.invoice_id.cod_doc_ref != '13':
                info_reference.set_Codigo(self.invoice_id.cod_referencia_id.code or "01")
                info_reference.set_Razon(self.invoice_id.reason_ref or "Anulacion")
            if info_reference.get_TipoDoc() == "99":
                info_reference.set_TipoDocRefOTRO("DOCUMENTO INTERNO")
                info_reference.set_CodigoReferenciaOTRO("DOCUMENTO INTERNO REFERENCIA")
        elif self.invoice_id and self.voucher_type_code == '08':
            info_reference.set_TipoDoc("16")
            info_reference.set_Numero(self.invoice_id.ref or 'SN')
            info_reference.set_FechaEmision(self.get_time_now_cr())
            if cedoc.get_Emisor().get_Identificacion().get_Tipo() == '05':
                info_reference.set_Codigo('11')
            else:
                info_reference.set_Codigo('04')

            info_reference.set_Razon('Documento original aportado por el contribuyente.')
        elif self.invoice_id and self.voucher_type_code == '10':
            info_reference.set_TipoDoc("01")
            info_reference.set_Numero(self.invoice_id.l10n_cr_document_name)
            info_reference.set_FechaEmision(self.date_issue_ref or self.get_time_now_cr())
            if cedoc.get_Emisor().get_Identificacion().get_Tipo() == '05':
                info_reference.set_Codigo('11')
            else:
                info_reference.set_Codigo('04')

            info_reference.set_Razon('Pago de factura de crédito')

        cedoc.add_InformacionReferencia(info_reference)

    def get_taxed_amount_data(self, lines):
        """Invoice amounts related values.

        Código del impuesto la tarifa del impuesto, Nota #8
        01 IVA
        02 Impuesto Selectivo de Consumo
        03 Impuesto Unico a los Combustibles
        04 Impuesto específico de Bebidas Alcoholicas
        05 Impuesto especifico sobre las bebidas envasadas sin contenido alcoholico y jabones de tocador
        06 Impuesto a los productos de tabaco
        07 IVA (calculo especial)
        08 IVA Regimen de Bienes Usados (Factor)
        12 Impuesto especifico al cemento
        99 Otros

        Código de la tarifa del IVA
        01 Tarifa 0% (Exento)
        02 Tarifa Reducida 1%
        03 Tarifa reducida 2%
        04 Tarifa reducida 4%
        05 Transitorio 0%
        06 Transitorio 4%
        07 Transitorio 8%
        08 Tarifa General 13%
        09 Tarifa reducida 0.5%
        10 Tarifa Exenta

        :param list lines: Lines of document.
        """

        iva_data = {
            "total_taxed_amount": 0,
            "02_taxed_base": 0,
            "03_taxed_base": 0,
            "04_taxed_base": 0,
            "05_taxed_base": 0,
            "06_taxed_base": 0,
            "07_taxed_base": 0,
            "08_taxed_base": 0,
            "09_taxed_base": 0,
            "10_taxed_base": 0,

            "02_taxed_amount": 0,
            "03_taxed_amount": 0,
            "04_taxed_amount": 0,
            "05_taxed_amount": 0,
            "06_taxed_amount": 0,
            "07_taxed_amount": 0,
            "08_taxed_amount": 0,
            "09_taxed_amount": 0,
            "10_taxed_amount": 0,
            "exempt_amount": 0,
        }

        tax_data = [
            line.tax_ids.compute_all(
                price_unit=line.price_subtotal,
                currency=line.currency_id,
                product=line.product_id,
                partner=self.partner_id,
                handle_price_include=False,
            )
            for line in self._iterable_products_xml(lines)
        ]

        iva_data["total_taxed_amount"] = sum(
            line["total_excluded"] for line in tax_data
        )

        for line_taxes in tax_data:
            for tax in line_taxes["taxes"]:
                if not tax["amount"]:
                    iva_data["exempt_amount"] += tax["base"]

                tax_id = self.env["account.tax"].browse(tax["id"])
                if tax_id.iva_tax_rate == '02':
                    iva_data["02_taxed_base"] += tax["base"]
                    iva_data["02_taxed_amount"] += tax["amount"]
                if tax_id.iva_tax_rate == '03':
                    iva_data["03_taxed_base"] += tax["base"]
                    iva_data["03_taxed_amount"] += tax["amount"]
                if tax_id.iva_tax_rate == '04':
                    iva_data["04_taxed_base"] += tax["base"]
                    iva_data["04_taxed_amount"] += tax["amount"]
                if tax_id.iva_tax_rate == '05':
                    iva_data["05_taxed_base"] += tax["base"]
                    iva_data["05_taxed_amount"] += tax["amount"]
                if tax_id.iva_tax_rate == '06':
                    iva_data["06_taxed_base"] += tax["base"]
                    iva_data["06_taxed_amount"] += tax["amount"]
                if tax_id.iva_tax_rate == '07':
                    iva_data["07_taxed_base"] += tax["base"]
                    iva_data["07_taxed_amount"] += tax["amount"]
                if tax_id.iva_tax_rate == '08':
                    iva_data["08_taxed_base"] += tax["base"]
                    iva_data["08_taxed_amount"] += tax["amount"]
                if tax_id.iva_tax_rate == '09':
                    iva_data["09_taxed_base"] += tax["base"]
                    iva_data["09_taxed_amount"] += tax["amount"]
                if tax_id.iva_tax_rate == '10':
                    iva_data["10_taxed_base"] += tax["base"]
                    iva_data["10_taxed_amount"] += tax["amount"]

        return iva_data

    def sign_doc(self, filename, ceconfig):
        if ceconfig.state == 'expired':
            action = self.env.ref("base.action_res_company_form")
            msg = _("Certificate is expired.")
            raise RedirectWarning(msg, action.id, _("Go to Setting"))

        if ceconfig.state == 'valid' and (0 < ceconfig.days_to_expire() <= 0):
            "Si el certificado esta verificado y los dias restante de vencimiento es 0."
            ceconfig.write({'state': 'expired'})
            action = self.env.ref("base.action_res_company_form")
            msg = _("Certificate days to expired.")
            raise RedirectWarning(msg, action.id, _("Go to Setting"))

        ce_name = self.name
        # args = 'mv ' + filename
        # args = args.split()
        # signed_filename = "/tmp/{}.xml".format(ce_name)
        # args.append(signed_filename)
        # subprocess.run(args)
        # xml_f = open(signed_filename, 'rb')
        # xml_file = xml_f.read()
        # xml_encoded = bytes(xml_file)
        # subprocess.call(['rm', '-f', signed_filename])

        import os
        import shutil
        temp_dir = tempfile.gettempdir()  # Usará la carpeta temporal correcta según el sistema
        signed_filename = os.path.join(temp_dir, f"{ce_name}.xml")
        # Usar shutil.move en lugar de `mv`
        shutil.move(filename, signed_filename)
        # Leer el archivo
        with open(signed_filename, 'rb') as xml_f:
            xml_file = xml_f.read()

        xml_encoded = bytes(xml_file)  # No es necesario esto si ya es bytes
        # Eliminar el archivo temporal (usando os.remove en lugar de 'rm')
        os.remove(signed_filename)

        hacienda_api = HaciendaApi(company_id=self.company_id)
        try:
            xml_signed = hacienda_api.generate_signature(xml_encoded, HACIENDA_RESOLUTION_URL)
        except Exception as e:
            _logger.error(e)
            raise UserError('Error al firmar. Compruebe las credenciales.')

        _logger.info("##### CE FIRMADO: " + signed_filename)

        if not self.xml_file:
            self.write({
                "xml_file": base64.b64encode(xml_signed),
                "xml_file_name": "%s_%s.xml" % (VOUCHER_TYPE_ABBR[self.voucher_type_code], self.number),
            })
        self.generate_qr_code(self.name)
        xml_f.close()
        return True

    def generate_qr_code(self, name):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
        qr.add_data(name)
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qrcode_img = base64.b64encode(buffer.getvalue())
        self.QR_code = qrcode_img

    def _l10n_cr_check_documents_for_send(self):
        """ Ensure the current records are eligible for sent to Hacienda.

                """
        failed_documents = self.filtered(
            lambda o: (not o.company_id.l10n_cr_auth_user or not o.company_id.l10n_cr_auth_pass)
                      and o.company_id.country_code == 'CR')
        if failed_documents:
            invoices_str = ", ".join(failed_documents.mapped('name'))
            raise UserError(_("Documents %s not selected an interface in a company.", invoices_str))

        invoices = self
        return invoices

    def get_origin_name(self):
        return self.invoice_id and self.invoice_id.name or ''

    @staticmethod
    def limit(literal, limit):
        return (literal[:limit - 3] + '...') if len(literal) > limit else literal

    def get_time_now_cr(self):
        now_utc = datetime.now(pytz.timezone('UTC'))
        now_cr = now_utc.astimezone(pytz.timezone('America/Costa_Rica'))
        return now_cr

    def get_partner_vat(self, partner):
        inv_cedula = str(partner.vat).zfill(12)
        cedula_emisor = self.limit(inv_cedula, 20)
        return cedula_emisor

    @api.model
    def _send_xml_to_MH(self, max_doc=10):
        if self:
            documents = self
        else:
            documents = self.search([('ind_state', 'in', ['not_sent'])], order='id', limit=max_doc)
        _logger.info('\n_sendXMLtoMH\n %r \n\n', documents)

        if not documents:
            return
        for doc in documents:
            company_id = doc.company_id
            hacienda_api = HaciendaApi(company_id=company_id)
            if not doc.xml_file:
                doc.action_gen_xml()
            if not doc.xml_file:
                doc.message_post(subject='Informacion:', body='Registro sin XML, no se pudo crear el archivo.')
            else:
                post_json = hacienda_api.postMH(doc, doc.get_time_now_cr().strftime("%Y-%m-%dT%H:%M:%S-06:00"))
                response_status = post_json.get('status')
                response_text = post_json.get('text')
                if 200 <= response_status <= 299:
                    doc.state = 'sent'
                    doc.ind_state = 'procesando'
                elif response_status == 429:
                    raise UserError(str(response_text))
                else:
                    if response_text.find('ya fue recibido anteriormente') != -1:
                        doc.state = 'sent'
                        doc.ind_state = 'procesando'
                        doc.message_post(
                            subject='Informacion:',
                            body='Ya recibido anteriormente, se pasa a consultar')
                    else:
                        doc.ind_state = 'error'
                        doc.message_post(subject='Error', body=response_text)

    @api.model
    def _send_request_to_MH(self, max_doc=10, max_dias=1, tipo=None):
        """Consultar Facturas Hacienda"""

        if self:
            documents = self
        else:
            fecha_origen = datetime.now() - timedelta(days=max_dias)
            list_domain = ['recibido', 'procesando']
            if tipo:
                list_domain = tipo
            documents = self.search([
                ('ind_state', 'in', list_domain),
                ('create_date', '>=', fecha_origen)
            ], order='id', limit=max_doc)
        _logger.info('\n_enviarMH\n %r \n\n', documents)

        if not documents:
            return

        for doc in documents:
            company_id = doc.company_id
            hacienda_api = HaciendaApi(company_id=company_id)
            get_json = hacienda_api.getMH(doc)
            status = get_json['status']
            if 200 <= status <= 299:
                doc.ind_state = get_json.get('ind-estado')
                doc.state = 'accepted' if get_json.get('ind-estado') == 'aceptado' else 'partially'
            elif status == 400:
                _logger.warning('Documento:%s no encontrado en Hacienda.  Estado: %s', doc.number,
                                get_json.get('ind-estado'))
                continue
            else:
                _logger.error('Documento: - Error inesperado en Consulta Hacienda - Abortando')
                continue
            if get_json.get('respuesta-xml'):
                doc.write({
                    'xml_mh_file_name': 'MH_%s.xml' % doc.name,
                    'xml_mh_file': get_json.get('respuesta-xml'),
                    'message_detail': self.getDetalleMensaje(get_json.get('respuesta-xml')),
                })

    def getDetalleMensaje(self, xml_mh_file):
        message = ''
        try:
            # DetalleMensaje
            xml = str(base64.b64decode(xml_mh_file).decode())
            string_xml_repl = re.sub(' xmlns="[^"]+"', '', xml, count=1)  # Remplaza xmlns por un vacio
            root = ET.fromstring(string_xml_repl)
            message = root.findall('DetalleMensaje')[0].text
        except Exception as e:
            _logger.error('Error al obtener el detalle del mensaje: %s', e)
        return message

    @api.model
    def _send_mail(self, max_mails=10, max_dias=1):
        """Envia email al cliente. De forma masiva (cron) o para un solo registro (Bton Send Email).

            """

        def _set_attachment_data(doc, email_template, voucher_type_name):
            # Se agregan los documentos nuevamente en vista de que los metodos anteriores fallaron
            # Adjuntos
            ir_attachment = self.env['ir.attachment'].sudo()
            xml_vals = {'name': str(doc.xml_file_name),
                        'datas': doc.xml_file,
                        'res_id': doc.id,
                        'res_model': self._name,
                        'type': 'binary',
                        }
            attachment_xml_file = ir_attachment.create(xml_vals)
            xml_mh_vals = {'name': str(doc.xml_mh_file_name),
                           'datas': doc.xml_mh_file,
                           'res_id': doc.id,
                           'res_model': self.name,
                           'type': 'binary',
                           }
            attachment_xml_mh = ir_attachment.create(xml_mh_vals)
            attachment_ids = []
            if attachment_xml_file:
                attachment_ids.append(attachment_xml_file.id)
            if attachment_xml_mh:
                attachment_ids.append(attachment_xml_mh.id)

            if attachment_ids:
                email_template.attachment_ids = [Command.set(attachment_ids)]
                email_template.subject = "{{ object.company_id.name }} Factura (Ref {{ object.name or 'n/a' }})"
                email_template.with_context(type='binary', default_type='binary').send_mail(
                    doc.invoice_id.id, raise_exception=False, force_send=True)

                # Se eliminan los archivos creados previamente para no generar basura
                attachment_xml_file.unlink()
                attachment_xml_mh.unlink()
                email_template.attachment_ids = [Command.clear()]
                doc.state_mail = 'sent'
                doc.message_post(subject='Email', body=f'{voucher_type_name} enviada')

        if self:
            documents = self
        else:
            date_origin = datetime.now() - timedelta(days=max_dias)
            documents = self.search([
                ('ind_state', '=', 'aceptado'),
                ('create_date', '>=', date_origin),
                ('state_mail', 'not in', ['sent', 'not_mail'])], order='id', limit=max_mails)

        _logger.info('\n\n %r \n\n', documents)
        if not documents:
            return

        for doc in documents:
            voucher_type_name = doc.voucher_type_id and doc.voucher_type_id.name or 'Factura'
            if doc.invoice_id and doc.partner_id and doc.partner_id.email:
                email_template = self.env.ref(
                    'account.email_template_edi_invoice', False)
                if email_template:
                    email_template.attachment_ids = [Command.clear()]
                else:
                    _logger.warning('El template de factura de email no existe')
                    continue

                _set_attachment_data(doc, email_template, voucher_type_name)
            elif doc.partner_id and doc.partner_id.email:
                email_template = self.env.ref(
                    'l10n_cr_invoice.email_template_document', False)
                if email_template:
                    email_template.attachment_ids = [Command.clear()]
                else:
                    _logger.warning('El template de factura de email no existe')
                    continue

                _set_attachment_data(doc, email_template, voucher_type_name)
            if not doc.partner_id.email:
                doc.state_mail = 'not_mail'
                doc.message_post(subject='Email', body=f'{voucher_type_name} no enviado, la empresa no tiene email')


class DocumentReference(models.Model):
    _name = 'ce.reference'
    _description = 'Document Reference'

    name = fields.Char('Name')
    ref_doctype = fields.Many2one('ce.reference.document', string='Document Reference Type', required=True)
    ref_number = fields.Char(string='Reference Number', required=True)
    ref_date = fields.Datetime(string='Reference Creation Date', required=True)
    ref_code = fields.Many2one('ce.reference.code', string='Reference Code', required=True)
    ref_reason = fields.Char(string='Reference Reason', required=False)
    company_id = fields.Many2one('res.company', string='Company', required=True)

    def action_view_document_reference(self):
        self.ensure_one()
        ref_number = self.ref_number

        return {
            'type': 'ir.actions.act_window',
            'name': _('Document Reference'),
            'res_model': 'ce.document',
            'view_mode': 'list,form',
            'domain': [('name', '=', ref_number)],
        }

    def action_download_file(self):
        """ Download the XML file linked to the document.

        :return: An action to download the attachment.
        """
        self.ensure_one()
        reference_id = self.env["ce.document"].search([('name', '=', self.ref_number)], limit=1)
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/ce.document/{reference_id.id}/xml_file/?download=true&filename={reference_id.xml_file_name}',
        }
