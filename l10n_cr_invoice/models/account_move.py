# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError, ValidationError, RedirectWarning
from lxml import etree
from datetime import datetime
import logging
import phonenumbers
import pytz
import random
_logger = logging.getLogger(__name__)
parser = etree.XMLParser(remove_blank_text=True)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def default_get(self, fields_list):
        result = super(AccountMove, self).default_get(fields_list)
        economic_activity_ids = self.env.company.l10n_cr_economic_activity_ids
        result['economic_activity_id'] = economic_activity_ids and economic_activity_ids[0].id or False
        return result

    l10n_cr_situation = fields.Selection(
        [('normal', 'Normal'),
         ('contingency', 'Contingencia'),
         ('no_internet', 'Sin Internet'),
         ],
        string="Status Voucher", required=True, default='normal')
    terminal_id = fields.Many2one('ce.terminal', string="Terminal", copy=False,
                                  help="Terminal o punto de venta.")
    document_id = fields.Many2one('ce.document', string="Document", readonly=True, copy=False)
    ind_state = fields.Selection(string="Hacienda State", related="document_id.ind_state", readonly=True, store=True)
    l10n_cr_message_detail = fields.Text(string="Detalle del Mensaje", related="document_id.message_detail")
    l10n_cr_document_number = fields.Char(string='Document Number', copy=False)
    l10n_cr_document_name = fields.Char(string='Key numeric', copy=False)
    # journal_pay_ids = fields.Many2many('account.journal',
    #                                    'invoice_journal_rel', 'invoice_id', 'journal_id',
    #                                    string="Medio de pago")
    l10n_cr_payment_method_id = fields.Many2one('l10n_cr.payment_method', compute="_compute_l10n_cr_payment_method_id",
                                                string="Payment Way", store=True, readonly=False, precompute=True)
    l10n_cr_payment_method_ids = fields.Many2many('l10n_cr.payment_method', 'payment_method_rel', 'invoice_id',
                                                  'payment_method_id', compute="_compute_l10n_cr_payment_method_ids",
                                                  string="Medio de pago", store=True, readonly=False, precompute=True)
    payment_term_type_id = fields.Many2one("ce.payment.term.type", "Condition Sale",
                                           compute="_compute_l10n_cr_payment_term_type_id", store=True)
    amount_discount = fields.Monetary(store=True, readonly=True, compute='_compute_amount',
                                      tracking=True)
    # amount_exonerated = fields.Monetary(string="Monto Exonerado", readonly=True)
    QR_code = fields.Binary(string="QR", related="document_id.QR_code")
    xml_amount_total = fields.Monetary(string="Monto total de documento")
    xml_amount_tax = fields.Monetary(string="Monto total de impuestos")
    is_exportation = fields.Boolean(string="Exportation Invoice", compute="_compute_l10n_cr_is_exportation", store=True)
    # l10n_cr_is_rep = fields.Boolean(string="Electronic Payment Receipt", compute="_compute_l10n_cr_is_rep", store=True)
    currency_rate = fields.Float(string="Tipo de cambio", compute='_compute_l10n_cr_currency_rate', readonly=False, store=True)
    voucher_type_id = fields.Many2one("ce.voucher.type", string="Voucher Type", compute='_compute_l10n_cr_voucher_type',
                                      store=True, readonly=False, auto_join=True, index=True)
    l10n_cr_available_voucher_type_ids = fields.Many2many('ce.voucher.type',
                                                          compute='_compute_l10n_cr_available_document_types')
    l10n_cr_fiscal_journal = fields.Boolean(related='journal_id.l10n_cr_fiscal_journal')
    l10n_cr_has_exoneration = fields.Boolean(compute="_compute_l10n_cr_has_exoneration")
    economic_activity_id = fields.Many2one('ce.economic.activity', string="Economic Activity", ondelete="restrict")
    l10n_cr_buyer_activity_id = fields.Many2one('ce.economic.activity', string="Buyer Economic Activity", store=True,
                                                ondelete="restrict", compute="_compute_l10n_cr_buyer_activity_id")
    l10n_cr_available_economic_activities_ids = fields.Many2many('ce.economic.activity',
                                                                 compute='_compute_l10n_cr_available_economic_activities')
    xml_file = fields.Binary("XML File", related="document_id.xml_file")

    # Reference
    tipo_doc_reference_id = fields.Many2one('ce.reference.document',
                                            string="Tipo de documento de referencia",
                                            copy=False,
                                            ondelete="restrict")
    cod_doc_ref = fields.Char(related="tipo_doc_reference_id.code", store=True, readonly=True, copy=False)
    cod_referencia_id = fields.Many2one('ce.reference.code',
                                        string="Códigos de referencia",
                                        copy=False,
                                        ondelete="restrict")
    reason_ref = fields.Char(string="Razon de referencia", copy=False)
    date_issue_ref = fields.Datetime(string="Fecha y hora de emision del documento de referencia", copy=False)
    numero_ref = fields.Char("Clave numérica de referencia",
                             help='Clave numérica del comprobante electrónico o consecutivo del documento de referencia',
                             copy=False)

    # MensajeReceptor
    state_inv_supplier = fields.Selection(
        [('1', 'Aceptado'),
         ('2', 'Aceptación parcial'),
         ('3', 'Rechazado'),
         ], string="Respuesta cliente", default="1")
    xml_mh_file = fields.Binary(attachment=True, string="Message Receptor File",
                                help="This field holds the XML file generated and signed by system")
    xml_mh_file_name = fields.Char("Name of XML Message Receptor File")
    l10n_cr_mh_send_state = fields.Selection([('accepted', 'Accepted'),
                                              ('reject', 'Reject')], string="Estado Hacienda")

    l10n_cr_reference_rep_ids = fields.Many2many('ce.reference', string='Reference Documents')

    # === COMPUTE METHODS ===#

    @api.depends('partner_id')
    def _compute_l10n_cr_has_exoneration(self):
        for move in self:
            move.l10n_cr_has_exoneration = True if move.partner_id.l10n_cr_exoneration_authorization else False

    @api.depends("journal_id", "voucher_type_id")
    def _compute_l10n_cr_is_exportation(self):
        for rec in self.filtered(lambda x: x.journal_id and x.journal_id.l10n_cr_fiscal_journal):
            rec.is_exportation = rec.voucher_type_id and rec.voucher_type_id.code == '09' or False

    # @api.depends("journal_id", "voucher_type_id")
    # def _compute_l10n_cr_is_rep(self):
    #     for rec in self.filtered(lambda x: x.journal_id and x.journal_id.l10n_cr_fiscal_journal):
    #         rec.l10n_cr_is_rep = rec.voucher_type_id and rec.voucher_type_id.code == '10' or False

    @api.depends('journal_id', 'company_id')
    def _compute_l10n_cr_available_economic_activities(self):
        self.l10n_cr_available_economic_activities_ids = False
        for rec in self:
            rec.l10n_cr_available_economic_activities_ids = self.env['ce.economic.activity'].search(
                rec._get_l10n_cr_economic_activities_domain())

    @api.depends('journal_id', 'company_id', 'move_type')
    def _compute_l10n_cr_available_document_types(self):
        self.l10n_cr_available_voucher_type_ids = False
        for rec in self.filtered(lambda x: x.journal_id and x.company_id.country_id == self.env.ref("base.cr")
                                           and x.journal_id.l10n_cr_fiscal_journal):
            domain = []
            if rec.move_type in ['out_refund', 'in_refund']:
                internal_types = ['credit_note']
            else:
                internal_types = ['invoice', 'debit_note']
            domain.append(('internal_type', 'in', internal_types))
            if rec.move_type == 'out_invoice':
                domain.append(('move_type', '=?', 'out_invoice'))
            elif rec.move_type == 'in_invoice':
                domain.append(('move_type', '=?', 'in_invoice'))
            # elif rec.move_type == 'out_receipt':
            #     domain.append(('move_type', '=?', 'out_receipt'))
            voucher_types = self.env["ce.voucher.type"].search(domain)
            rec.l10n_cr_available_voucher_type_ids = voucher_types

    @api.depends('move_type', 'debit_origin_id', 'partner_id')
    def _compute_l10n_cr_voucher_type(self):
        # for rec in self.filtered(lambda x: x.move_type in ['out_invoice', 'in_invoice', 'out_refund', 'in_refund', 'out_receipt']
        for rec in self.filtered(lambda x: x.move_type in ['out_invoice', 'in_invoice', 'out_refund', 'in_refund']
                                           and x.company_id.country_id == self.env.ref("base.cr")):
            sequence = {
                'out_invoice': '01',
                'out_refund': '03',
                'in_refund': '03',
                'in_invoice': '08',
                # 'out_receipt': '10',
            }

            if rec.is_exportation:
                code = '09'
            # elif rec.l10n_cr_is_rep:
            #     code = '10'
            elif rec.debit_origin_id:
                code = "02"
            elif rec.partner_id and not rec.partner_id.vat and rec.move_type in ['out_invoice', 'in_invoice']:
                code = "04"
            else:
                code = sequence[rec.move_type]

            voucher_type_id = self.env['ce.voucher.type'].search([('code', '=', code)])
            rec.voucher_type_id = voucher_type_id and voucher_type_id[0].id or False

    @api.depends('partner_id.l10n_cr_activity_id')
    def _compute_l10n_cr_buyer_activity_id(self):
        for rec in self.filtered(lambda x: x.company_id.country_id == self.env.ref("base.cr")):
            rec.l10n_cr_buyer_activity_id = rec.partner_id.l10n_cr_activity_id and rec.partner_id.l10n_cr_activity_id.id or False

    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()
        for inv in self:
            if inv.is_invoice(include_receipts=False):
                line_total_discount = sum(
                    (line.price_unit * line.quantity * line.discount / 100) for line in inv.invoice_line_ids)
                total_discount = line_total_discount
                inv.amount_discount = total_discount

    @api.depends("invoice_payment_term_id")
    def _compute_l10n_cr_payment_term_type_id(self):
        for record in self:
            if record.invoice_payment_term_id:
                record.payment_term_type_id = record.invoice_payment_term_id.payment_type_id
            else:
                cash = self.env.ref("l10n_cr_invoice.payment_type_01", False)
                record.payment_term_type_id = cash and cash.id

    @api.depends("move_type")
    def _compute_l10n_cr_payment_method_id(self):
        for move in self.filtered(lambda r: r.l10n_cr_fiscal_journal and r.country_code == 'CR'):
            if not move.l10n_cr_payment_method_id:
                default_payment_method = self.env['l10n_cr.payment_method'].search([('code', '=', '01')], limit=1)
                move.l10n_cr_payment_method_id = default_payment_method.id

    @api.depends("move_type")
    def _compute_l10n_cr_payment_method_ids(self):
        for move in self.filtered(lambda r: r.l10n_cr_fiscal_journal and r.country_code == 'CR'):
            if not move.l10n_cr_payment_method_ids:
                default_payment_methods = self.env['l10n_cr.payment_method'].search([('code', '=', '01')], limit=1)
                move.l10n_cr_payment_method_ids = [Command.set(default_payment_methods.ids)]

    @api.depends('currency_id', 'company_id')
    def _compute_l10n_cr_currency_rate(self):
        for record in self:
            if record.is_invoice(include_receipts=False) and record.l10n_cr_fiscal_journal and record.currency_id:
                date = record.invoice_date or record.date or fields.Date.context_today(record)
                rate = record.currency_id.with_context(dict(record._context or {}, date=date)).rate
                rate = round(1.0 / rate, 5)
                record.currency_rate = rate
            else:
                record.currency_rate = 1

    # === BUSINESS METHODS ===#

    @api.constrains("state", "voucher_type_id", "partner_id")
    def validate_l10n_cr_voucher_type(self):
        for inv in self.filtered(
                lambda i: i.move_type == "out_invoice" and i.state == "posted" and i.l10n_cr_fiscal_journal):
            if inv.voucher_type_id.code == '01':
                if inv.partner_id.identification_id and inv.partner_id.identification_id.code == '05':
                    raise UserError("FE no aplica para clientes con tipo de identificación extranjero.")

    @api.constrains("move_type", "voucher_type_id")
    def _l10n_cr_check_invoice_type_voucher_type(self):
        """Define that we are not able to use debit_note or invoice document types in an invoice refunds"""
        for rec in self.filtered('voucher_type_id.internal_type'):
            internal_type = rec.voucher_type_id.internal_type
            invoice_type = rec.move_type
            if internal_type in ['debit_note', 'invoice'] and invoice_type in ['out_refund', 'in_refund']:
                raise ValidationError(_('You can not use a %s document type with a refund invoice', internal_type))
            elif internal_type == 'credit_note' and invoice_type in ['out_invoice', 'in_invoice']:
                raise ValidationError(_('You can not use a %s document type with a invoice', internal_type))

        for rec in self.filtered(
                lambda r: r.company_id.country_id == self.env.ref("base.cr") and r.voucher_type_id
        ):
            partner = rec.partner_id
            voucher_type_id = rec.voucher_type_id

            # if partner.identification_id.code == "05" and voucher_type_id.code != "08":
            #     raise UserError(_('El código del tipo "Extranjero No Domiciliado" solo se permite en la FEC.'))
            #
            # if partner.identification_id.code == "06" and voucher_type_id.code != "08":
            #     raise UserError(_('El código del tipo "No Contribuyente" sol se permite en la FEC.'))

            if voucher_type_id.code == "09" and partner.l10n_cr_exoneration_authorization:
                raise UserError(_("No debe de ser utilizado exoneraciones en el tipo de comprobante “Factura electrónica de Exportación”"))

    def _get_invoice_report_filename(self, extension='pdf'):
        """ Get the filename of the generated invoice report with extension file. """
        self.ensure_one()
        if self.l10n_cr_fiscal_journal and self.country_code == 'CR' and self.document_id:
            # return self.document_id.name
            return self.document_id.number

        return super()._get_invoice_report_filename(extension)

    def _get_report_base_filename(self):
        self.ensure_one()
        if self.l10n_cr_fiscal_journal and self.country_code == 'CR':
            return self._get_invoice_report_filename()

        return super()._get_report_base_filename()

    def _get_l10n_cr_economic_activities_domain(self):
        self.ensure_one()
        company_id = self.company_id
        domain = [('id', 'in', company_id.l10n_cr_economic_activity_ids.ids)]
        return domain

    @api.onchange('tipo_doc_reference_id')
    def change_tipo_documento_referencia(self):
        if self.tipo_doc_reference_id and self.tipo_doc_reference_id.code == '08':
            self.cod_referencia_id = self.env.ref('l10n_cr_invoice.reference_code_05')

    def _post(self, soft=True):
        for inv in self.filtered(lambda x: x.move_type not in ('entry',)):
            if inv.l10n_cr_fiscal_journal and inv.country_code == 'CR':
                if not inv.voucher_type_id:
                    error_msg = _(
                        "No Voucher Type could be found",
                    )
                    raise UserError(error_msg)

                if not inv.terminal_id:
                    # Si no hay terminal en la factura, se establece la primera terminal activa de la compañia.
                    terminal_id = self.env["ce.terminal"].search([('company_id', '=', inv.company_id.id),
                                                                  ('state', '=', 'active')], limit=1)
                    if not terminal_id:
                        raise ValidationError(_("There is not active Terminal"))

                    inv.terminal_id = terminal_id

        res = super(AccountMove, self)._post(soft)
        invoices = self._l10n_cr_check_moves_for_send()
        for inv in invoices.filtered(lambda x: x.move_type not in ('entry',)):
            if inv.l10n_cr_fiscal_journal and inv.country_code == 'CR':
                # if inv.move_type in ['out_invoice', 'in_invoice', 'out_refund', 'in_refund', 'out_receipt']:
                if inv.move_type in ['out_invoice', 'in_invoice', 'out_refund', 'in_refund']:
                    if not inv.l10n_cr_document_number:
                        inv.l10n_cr_document_number = inv.terminal_id.gen_consecutive_number(inv.voucher_type_id)
                    if not inv.l10n_cr_document_name:
                        inv.l10n_cr_document_name = self.gen_key_numeric(inv.l10n_cr_document_number)
                    if not inv.document_id:
                        inv.l10n_cr_create_document(terminal_id=inv.terminal_id)
                    elif inv.document_id and inv.document_id.ind_state == 'rechazado':
                        inv.l10n_cr_recreate_document()

                    document_number = inv.l10n_cr_document_name
                    inv.write(
                        {
                            "payment_reference": '%s - %s' % (inv.name, document_number),
                        }
                    )
        # TODO: Mostrar los errores como en el conector de RD.
        return res

    def _l10n_cr_check_moves_for_send(self):
        """ Ensure the current records are eligible for sent to Hacienda.

                """
        failed_moves = self.filtered(
            lambda o: o.l10n_cr_fiscal_journal and (not o.company_id.l10n_cr_auth_user or not o.company_id.l10n_cr_auth_pass)
                      and o.country_code == 'CR')
        if failed_moves:
            invoices_str = ", ".join(failed_moves.mapped('name'))
            raise UserError(_("Invoices %s not eligible to sent (Not exist credentials to auth)", invoices_str))

        invoices = self
        return invoices

    def l10n_cr_receipt_payment_send(self, payment_date, memo):
        self.ensure_one()
        self.l10n_cr_create_document_rep(terminal_id=self.terminal_id, payment_date=payment_date, memo=memo)

    def l10n_cr_create_document_rep(self, terminal_id, payment_date=False, memo=False):
        voucher_type_id = self.env.ref("l10n_cr_invoice.voucher_10")
        payment_term_type_id = self.env.ref("l10n_cr_invoice.payment_type_11")
        l10n_cr_document_number = terminal_id.gen_consecutive_number(voucher_type_id)
        l10n_cr_key_numeric = self.gen_key_numeric(l10n_cr_document_number)
        Document = self.env['ce.document']
        default_data = (Document.with_context(force_economic_activity=self.economic_activity_id.id).
                        default_get(
            ['state', 'company_id', 'l10n_cr_situation', 'ind_state', 'economic_activity_id']))
        default_data.update(
            invoice_id=self.id,
            terminal_id=terminal_id.id,
            voucher_type_id=voucher_type_id.id,
            partner_id=self.partner_id.id,
            company_id=self.company_id.id,
            currency_id=self.currency_id.id,
            situation=self.l10n_cr_situation,
            number=l10n_cr_document_number,
            name=l10n_cr_key_numeric,
            payment_term_type_id=payment_term_type_id.id,
        )
        default_data.update({'invoice_type': 'out_receipt'})
        if self.l10n_cr_buyer_activity_id:
            default_data.update({'l10n_cr_buyer_activity_id': self.l10n_cr_buyer_activity_id.id})
        default_data.update(self._prepare_document_additional_values())
        doc_id = Document.create(default_data)
        doc_id.action_gen_xml()

        ref_type = self.env['ce.reference.document'].search([('code', '=', '01')], limit=1)
        ref_code = self.env['ce.reference.code'].search([('code', '=', '04')], limit=1)
        ref_doc_vals = {
            'name': memo,
            'ref_doctype': ref_type.id,
            'ref_number': doc_id.name,
            'ref_date': payment_date,
            'ref_code': ref_code.id,
            'company_id': self.company_id.id,
        }
        self.write({'l10n_cr_reference_rep_ids': [Command.create(ref_doc_vals)]})
        return doc_id

    def gen_key_numeric(self, number):
        partner_id = self.company_id.partner_id
        tel = partner_id.phone if partner_id.phone else partner_id.mobile
        if not tel:
            raise ValidationError(_('Company does not have a phone defined'))

        if not partner_id.vat:
            raise ValidationError(_('Company does not have a VAT defined'))

        phone = phonenumbers.parse(tel, 'CR')
        country_code = phone.country_code or 506
        now_utc = datetime.now(pytz.timezone('UTC'))
        now_cr = now_utc.astimezone(pytz.timezone('America/Costa_Rica'))
        dmy = now_cr.strftime("%d%m%y")
        cedula = self.env["ce.document"].get_partner_vat(self.company_id.partner_id)
        security_code = str(random.randint(1, 99999999)).zfill(8)
        if self.l10n_cr_situation == 'normal':
            situation = '1'
        elif self.l10n_cr_situation == 'contingency':
            situation = '2'
        elif self.l10n_cr_situation == 'no_internet':
            situation = '3'

        return "%s%s%s%s%s%s" % (country_code, dmy, cedula, number, situation, security_code)

    def l10n_cr_create_document(self, terminal_id, reference_nc=None, recreate=False):
        if not self.document_id or recreate:
            if recreate:
                self.l10n_cr_document_number = terminal_id.gen_consecutive_number(self.voucher_type_id)
                self.l10n_cr_document_name = self.gen_key_numeric(self.l10n_cr_document_number)
            Document = self.env['ce.document']
            default_data = (Document.with_context(force_economic_activity=self.economic_activity_id.id).
                            default_get(
                ['state', 'company_id', 'l10n_cr_situation', 'ind_state', 'economic_activity_id']))
            default_data.update(
                invoice_id=self.id,
                terminal_id=terminal_id.id,
                voucher_type_id=self.voucher_type_id.id,
                partner_id=self.partner_id.id,
                company_id=self.company_id.id,
                currency_id=self.currency_id.id,
                situation=self.l10n_cr_situation,
                number=self.l10n_cr_document_number,
                name=self.l10n_cr_document_name,
                payment_term_type_id=self.payment_term_type_id.id,
            )
            if self.env.context.get("invoice_type"):
                default_data.update({'invoice_type': self.env.context["invoice_type"]})
            else:
                default_data.update({'invoice_type': self.move_type})
            if self.l10n_cr_buyer_activity_id:
                default_data.update({'l10n_cr_buyer_activity_id': self.l10n_cr_buyer_activity_id.id})
            default_data.update(self._prepare_document_additional_values())
            doc_id = Document.create(default_data)
            if self.date_issue_ref:
                doc_id.date_issue_ref = self.date_issue_ref or None
            self.document_id = doc_id.id
            doc_id.action_gen_xml(reference_nc)
            return doc_id

    def _prepare_document_additional_values(self):
        """
            Prepare the dict of values to create the additional values a documents. This method may be
            overridden to implement custom document generation (making sure to call super() to establish
            a clean extension chain).
            """
        return {

        }

    def l10n_cr_recreate_document(self):
        if self.document_id and self.document_id.ind_state == 'rechazado':
            """Sustituye factura rechazada por el Ministerio de Hacienda
               y hace referencia al documento actual rechazado"""

            company_id = self.company_id.id
            ref_type = self.env['ce.reference.document'].search([('code', '=', '10')], limit=1)
            ref_code = self.env['ce.reference.code'].search([('code', '=', '01')], limit=1)
            ref_doc_vals = {
                'name': 'Sustituye factura rechazada por MH',
                'ref_doctype': ref_type.id,
                'ref_number': self.document_id.name,
                'ref_date': self.document_id.create_date,
                'ref_code': ref_code.id,
                'ref_reason': 'Sustituye factura rechazada por MH',
                'company_id': company_id,
            }
            if self.numero_ref:
                write_status = self.l10n_cr_create_document(terminal_id=self.terminal_id,
                                                            reference_nc=self.numero_ref,
                                                            recreate=True)
            else:
                write_status = self.l10n_cr_create_document(terminal_id=self.terminal_id, recreate=True)
            if write_status:
                self.document_id.write({'ref_ids': [Command.create(ref_doc_vals)], "is_ref": True})

            return write_status

    def ticket_print(self):
        return self.env.ref('l10n_cr_invoice.account_invoices_rollo').report_action(self)

    # ===== BUTTONS =====

    def button_draft(self):
        if self.l10n_cr_fiscal_journal and self.country_code == 'CR':
            if self.document_id and self.ind_state in ['aceptado', 'procesando', 'recibido']:
                raise UserError("No puede establecer a borrador una factura enviada a Hacienda.")
            elif self.document_id and self.ind_state in ['not_sent']:
                self.document_id.unlink()

        res = super(AccountMove, self).button_draft()
        return res

    def action_send_to_hacienda(self):
        invoices = self._l10n_cr_check_moves_for_send()
        for move in invoices:
            move.document_id.action_send_to_hacienda()

    def action_request_state_to_hacienda(self):
        invoices = self._l10n_cr_check_moves_for_send()
        for move in invoices:
            if move.document_id.xml_file:
                move.document_id.action_request_state_to_hacienda()
            else:
                raise UserError(_('Must be a xml file.'))
