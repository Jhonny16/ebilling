# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from .test_edi_common import TestL10nCREdiCommon


@tagged('post_install_l10n', 'post_install', '-at_install')
class TestCrAccountMove(TestL10nCREdiCommon):

    def test_l10n_cr_out_invoice_default_values_form(self):
        """Test prueba campos computados y valores por defecto
        en formulario de Factura de cliente"""
        self._setup_company_cr_issuer()
        journal = self.journal_sale.copy({"name": "Invoices Journal"})
        # self.assertTrue(self.AccountMove._fields["l10n_latam_internal_type"].store)
        form = self._l10n_cr_create_form_move(
            move_type="out_invoice",
            # internal_type="invoice",
            partner=self.partner_non_payer
        )
        self.assertIn(form.journal_id, journal + self.journal_sale)

    def test_l10n_cr_out_invoice_non_document(self):
        """Test prueba Factura de cliente no fiscal"""
        self._setup_company_cr()
        self.product_a.list_price = 250000.00
        form = self._l10n_cr_create_form_move(
            move_type="out_invoice",
            # internal_type="out_invoice",
            partner=self.partner_taxpayer,
        )

        invoice = form.save()
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")

    def test_l10n_cr_out_invoice_document_signed_FE(self):
        """Test prueba de Factura electronica. """
        self._setup_company_cr_issuer()
        self.product_a.list_price = 250000.00
        form = self._l10n_cr_create_form_move(
            move_type="out_invoice",
            # internal_type="out_invoice",
            partner=self.partner_taxpayer,
            use_payment_term=True,  # Uso CondicionVenta=02, PlazoCredito=15
        )

        invoice = form.save()
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.assertEqual(invoice.ind_state, "not_sent")
        self.assertTrue(invoice.document_id)
        self.assertEqual(invoice.document_id.invoice_type, "out_invoice")
        "Si no hay terminal en la factura, se establece la primera terminal activa de la compañia."
        self.assertEqual(invoice.document_id.terminal_id, self.terminal_id)

    def test_l10n_cr_out_invoice_document_signed_TE(self):
        """Test prueba de Tiquete electronico. """
        self._setup_company_cr_issuer()
        voucher_type_id = self.env.ref("l10n_cr_invoice.voucher_04")
        self.product_a.list_price = 250000.00
        form = self._l10n_cr_create_form_move(
            move_type="out_invoice",
            # internal_type="out_invoice",
            partner=self.partner_non_payer,
            voucher_type=voucher_type_id,
            terminal=self.terminal_id,
        )

        invoice = form.save()
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.assertEqual(invoice.ind_state, "not_sent")
        self.assertTrue(invoice.document_id)
        self.assertEqual(invoice.document_id.invoice_type, "out_invoice")
        self.assertEqual(invoice.document_id.voucher_type_id, voucher_type_id)
        self.assertEqual(invoice.document_id.terminal_id, self.terminal_id)

    # def test_l10n_cr_out_invoice_document_signed_TE_POS(self):
    #     """Test prueba de Tiquete electronico POS. """
    #     self._setup_company_cr_issuer()
    #     voucher_type_id = self.env.ref("l10n_cr_invoice.voucher_04")
    #     self.product_a.list_price = 250000.00
    #     form = self._l10n_cr_create_form_move(
    #         move_type="out_invoice",
    #         # internal_type="out_ticket",
    #         partner=self.partner_non_payer,
    #         voucher_type=voucher_type_id,
    #         terminal=self.terminal_id,
    #     )
    #
    #     invoice = form.save()
    #     invoice.action_post()
    #     self.assertEqual(invoice.state, "posted")
    #     self.assertEqual(invoice.ind_state, "not_sent")
    #     self.assertTrue(invoice.document_id)
    #     self.assertEqual(invoice.document_id.invoice_type, "out_ticket")
    #     self.assertEqual(invoice.document_id.voucher_type_id, voucher_type_id)
    #     self.assertEqual(invoice.document_id.terminal_id, self.terminal_id)

    def test_l10n_cr_out_invoice_document_signed_TEE(self):
        """Test prueba de Factura electronica exportacion. """
        self._setup_company_cr_issuer()
        voucher_type_id = self.env.ref("l10n_cr_invoice.voucher_09")
        self.product_a.list_price = 250000.00
        form = self._l10n_cr_create_form_move(
            move_type="out_invoice",
            # internal_type="out_invoice",
            partner=self.partner_taxpayer,
            voucher_type=voucher_type_id,
            terminal=self.terminal_id,
        )

        invoice = form.save()
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.assertEqual(invoice.ind_state, "not_sent")
        self.assertTrue(invoice.document_id)
        self.assertEqual(invoice.document_id.invoice_type, "out_invoice")
        self.assertEqual(invoice.document_id.voucher_type_id, voucher_type_id)
        self.assertEqual(invoice.document_id.terminal_id, self.terminal_id)

    def test_l10n_cr_out_invoice_document_signed_NC(self):
        """Test prueba de Nota Credito electronica. """
        self._setup_company_cr_issuer()
        voucher_type_id = self.env.ref("l10n_cr_invoice.voucher_03")
        self.product_a.list_price = 250000.00
        form = self._l10n_cr_create_form_move(
            move_type="out_refund",
            # internal_type="out_refund",
            partner=self.partner_taxpayer,
            voucher_type=voucher_type_id,
            terminal=self.terminal_id,
        )

        invoice = form.save()
        invoice.numero_ref = "XX"
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.assertEqual(invoice.ind_state, "not_sent")
        self.assertTrue(invoice.document_id)
        self.assertEqual(invoice.document_id.invoice_type, "out_refund")
        self.assertEqual(invoice.document_id.voucher_type_id, voucher_type_id)
        self.assertEqual(invoice.document_id.terminal_id, self.terminal_id)

    def test_l10n_cr_out_invoice_document_signed_FEC(self):
        """Test prueba de Factura electronica compra. """
        self._setup_company_cr_issuer()
        voucher_type_id = self.env.ref("l10n_cr_invoice.voucher_08")
        self.product_a.list_price = 250000.00
        form = self._l10n_cr_create_form_move(
            move_type="in_invoice",
            # internal_type="in_invoice",
            partner=self.partner_contact,
            voucher_type=voucher_type_id,
            terminal=self.terminal_id,
        )

        invoice = form.save()
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.assertEqual(invoice.ind_state, "not_sent")
        self.assertTrue(invoice.document_id)
        self.assertEqual(invoice.document_id.invoice_type, "in_invoice")
        self.assertEqual(invoice.document_id.voucher_type_id, voucher_type_id)
        self.assertEqual(invoice.document_id.terminal_id, self.terminal_id)
