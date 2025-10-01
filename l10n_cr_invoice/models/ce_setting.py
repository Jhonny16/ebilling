# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from base64 import b64decode
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from cryptography.x509.oid import ExtensionOID, NameOID
from ..hacienda_api import HaciendaApi
from odoo.exceptions import ValidationError, UserError
import requests

import logging
_logger = logging.getLogger(__name__)


class CeSetting(models.Model):
    _name = "cr.ce.setting"
    _inherit = ['portal.mixin', 'mail.thread']
    _description = "Electronic Vouchers Configuration"

    name = fields.Char(required=True, tracking=True)
    p12_file = fields.Binary(string="Llave Criptografica")
    p12_name = fields.Char(string="Llave Criptografica")
    p12_pin = fields.Char(string="PIN p12")
    company_id = fields.Many2one("res.company", string="Company", ondelete='cascade', tracking=True, readonly=True,
                                 default=lambda self: self.env.company)
    state = fields.Selection(
        [
            ("unverified", "Unverified"),
            ("valid", "Valid Signature"),
            ("expired", "Signature Expired"),
        ],
        default="unverified",
        readonly=True,
    )

    # datos informativos del certificado
    issue_date = fields.Date(string="Date of issue", readonly=True)
    expire_date = fields.Date(string="Expiration Date", readonly=True)
    subject_serial_number = fields.Char(string="Serial Number(Subject)", readonly=True)
    subject_common_name = fields.Char(string="Organization(Subject)", readonly=True)
    issuer_common_name = fields.Char(string="Organization (Issuer)", readonly=True)
    cert_serial_number = fields.Char(
        string="Serial number (certificate)", readonly=True
    )
    cert_version = fields.Char(string="Version", readonly=True)
    days_for_notification = fields.Integer(string="Days for notification", default=30)

    def _decode_certificate(self):
        self.ensure_one()
        if not self.p12_pin:
            return None, None
        file_content = b64decode(self.p12_file)
        try:
            private_key, cert, additional_certs = load_key_and_certificates(file_content,
                                                                            self.p12_pin.encode())

        except Exception as ex:
            _logger.warning(tools.ustr(ex))
            raise UserError(
                _(
                    "Error opening the signature, possibly the signature key has "
                    "been entered incorrectly or the file is not supported. \n%s"
                )
                % (tools.ustr(ex))
            ) from None
        return private_key, cert

    def action_validate_and_load(self):
        _private_key, cert = self._decode_certificate()
        issuer = cert.issuer
        subject = cert.subject
        subject_common_name = (
            subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            if subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            else ""
        )
        subject_serial_number = (
            subject.get_attributes_for_oid(NameOID.SERIAL_NUMBER)[0].value
            if subject.get_attributes_for_oid(NameOID.SERIAL_NUMBER)
            else ""
        )
        issuer_common_name = (
            issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            if subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            else ""
        )
        vals = {
            "issue_date": fields.Datetime.context_timestamp(
                self, cert.not_valid_before
            ).date(),
            "expire_date": fields.Datetime.context_timestamp(
                self, cert.not_valid_after
            ).date(),
            "subject_common_name": subject_common_name,
            "subject_serial_number": subject_serial_number,
            "issuer_common_name": issuer_common_name,
            "cert_serial_number": cert.serial_number,
            "cert_version": cert.version,
            "state": "valid",
        }
        self.write(vals)
        return True

    def days_to_expire(self):
        if self.expire_date:
            return (self.expire_date - fields.Date.context_today(self)).days
        return 0

    @api.model
    def action_email_notification(self):
        email_template = self.env.ref(
            "l10n_cr_invoice.email_template_notify", False
        )
        all_companies = self.env["res.company"].search([])
        for company in all_companies:
            certificates = self.search(
                [("company_id", "=", company.id), ("state", "=", "valid")]
            )
            for cert in certificates:
                if 0 < cert.days_to_expire() <= cert.days_for_notification:
                    _logger.info("Enviando notificacion de recordatorio de certificado..")
                    email_template.send_mail(
                        cert.id, email_layout_xmlid="mail.mail_notification_light"
                    )
        return True
