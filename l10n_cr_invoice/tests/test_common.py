# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo.tests import tagged, Form

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged('post_install_l10n', 'post_install', '-at_install')
class TestL10nCRCommon(AccountTestInvoicingCommon):

    @classmethod
    @AccountTestInvoicingCommon.setup_country('cr')
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.company_data["company"]
        
        # Models
        cls.Partner = cls.env["res.partner"].with_company(cls.company).sudo()
        cls.Journal = cls.env["account.journal"].with_company(cls.company)
        cls.AccountMove = cls.env["account.move"].with_company(cls.company)
        cls.current_datetime = fields.Datetime.context_timestamp(
            cls.AccountMove, fields.Datetime.now()
        )
        cls.current_date = fields.Date.context_today(cls.AccountMove)

        # Partners
        cls.partner_contact = cls.company.partner_id
        cls.partner_non_payer = cls.Partner.create(
            {
                "name": "Consumidor Final",
                "country_id": cls.env.ref("base.cr").id,
                "identification_id": cls.env.ref("l10n_cr_invoice.Identificationtype_01").id,
                "vat": "3102838754",
            }
        )
        cls.partner_taxpayer = cls.Partner.create(
            {
                "name": "INVERSIONES COMERCIAL DE IM&EX SOCIEDAD DE RESPONSABILIDAD LIMITADA",
                "country_id": cls.env.ref("base.cr").id,
                "vat": "3102838754",
                "email": "susivalenzuela@hotmail.com",
                "street": "SN",
                "identification_id": cls.env.ref("l10n_cr_invoice.Identificationtype_02").id,
                "state_id": cls.env.ref("base.state_SJ").id,
                "distrito_id": cls.env.ref("l10n_cr_address.district_Carmen_San_Jose_SJ").id,
                "canton_id": cls.env.ref("l10n_cr_address.county_San_Jose_SJ").id,
                "neighborhood_id": cls.env.ref("l10n_cr_address.neighborhood_Amon_Carmen_San_Jose_SJ").id,
            }
        )
        # Diarios
        cls.journal_sale = cls.company_data["default_journal_sale"]
        cls.journal_purchase = cls.company_data["default_journal_purchase"]

        cls.product_a.cabys_code = 2391100020200

    def _setup_company_cr(self):
        """Configurar datos para compañia dominicana"""
        self.company.write(
            {
                "vat": "3101881188",
                "currency_id": self.env.ref("base.CRC").id,
                "country_id": self.env.ref("base.cr").id,
            }
        )

    def _l10n_cr_create_form_move(
        self,
        move_type,
        partner,
        internal_type=None,
        taxes=None,
        products=None,
        journal=None,
        voucher_type=None,
        use_payment_term=False,
        terminal=False,
        form_id=None,
    ):
        """Método base con datos genericos para crear formulario de:
         Faturas, notas de crédito,debito, liquidaciones y retenciones de venta
        :param move_type: Tipo de documento (in_invoice,out_invoice,in_refund,
          out_refund)
        :param internal_type: Tipo interno del documento(invoice,credit_note)
        :param partner: Partner del documento
        :param number: Número del documento, si no se envia se coloca uno
        :param taxes: Impuestos, Por defecto se toma impuestos del producto
        :param products: Productos, si no se envia, se colocará un producto
        :param journal: Diario, si no se envia por defecto coloca uno
         según el internal_type y move_type; campo requerido
        :param latam_document_type: Tipo de documento, si no se envia por defecto
         coloca uno según el partner y journal; campo requerido
        :param use_payment_term: Si es True, colocará un término de pago en el
          documento, por defecto False
        :param form_id: ID del formulario si fuese diferente al de la factura,
          por defecto None
        """
        products = products or self.product_a
        move_form = Form(
            self.AccountMove.with_context(
                default_move_type=move_type,
                # invoice_type=internal_type,
                mail_create_nosubscribe=True,
            ),
            form_id,
        )

        move_form.invoice_date = fields.Date.context_today(self.AccountMove)
        move_form.partner_id = partner
        if journal:
            move_form.journal_id = journal
        if move_form.journal_id.l10n_cr_fiscal_journal and voucher_type:
            move_form.voucher_type_id = voucher_type
        if use_payment_term:
            move_form.invoice_payment_term_id = self.env.ref(
                "account.account_payment_term_15days"
            )
        if move_form.journal_id.l10n_cr_fiscal_journal and terminal:
            move_form.terminal_id = terminal
        for product in products or []:
            with move_form.invoice_line_ids.new() as line_form:
                line_form.product_id = product
                if taxes:
                    line_form.tax_ids.clear()
                    for tax in taxes:
                        line_form.tax_ids.add(tax)
        return move_form
