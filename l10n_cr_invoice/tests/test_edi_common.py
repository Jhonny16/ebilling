# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from odoo.tools import misc
import os

from .test_common import TestL10nCRCommon
import base64


@tagged('post_install_l10n', 'post_install', '-at_install')
class TestL10nCREdiCommon(TestL10nCRCommon):

    @classmethod
    @AccountTestInvoicingCommon.setup_country('cr')
    def setUpClass(cls):
        super().setUpClass()
        file_path = os.path.join(
            "l10n_cr_invoice", "tests", "certificates", "test.p12"
        )
        file_content = misc.file_open(file_path, mode="rb").read()
        # Crear certificado de firma electrónica válido
        cls.certificate = (
            cls.env["cr.ce.setting"]
            .sudo()
            .create(
                {
                    "name": "Test",
                    "p12_name": "test.p12",
                    "p12_pin": "6890",
                    "p12_file": base64.b64encode(file_content),
                    "company_id": cls.company_data["company"].id,
                },
            )
        )

    def _setup_company_cr_issuer(self):
        self._setup_company_cr()
        self.certificate.action_validate_and_load()
        self.Terminal = self.env["ce.terminal"].with_company(self.company).sudo()
        self.partner_contact.write(
            {
                "identification_id": self.env.ref("l10n_cr_invoice.Identificationtype_02").id,
                "street": "SN",
                "email": "loco@gmail.com",
                "phone": "+506 6339 7656",
                "state_id": self.env.ref("base.state_SJ").id,
                "distrito_id": self.env.ref("l10n_cr_address.district_Carmen_San_Jose_SJ").id,
                "canton_id": self.env.ref("l10n_cr_address.county_San_Jose_SJ").id,
                "neighborhood_id": self.env.ref("l10n_cr_address.neighborhood_Amon_Carmen_San_Jose_SJ").id,
                "vat": "3101881188"
            }
        )

        self.company.write(
            {
                "setting_id": self.certificate.id,
                "l10n_cr_economic_activity_ids": [(6, 0,
                                           [self.env["ce.economic.activity"].search([('code', '=', '722003')],
                                                                                    limit=1).id])],
            }
        )

        journal_vals = {
                "l10n_cr_fiscal_journal": True,
            }

        self.journal_sale.write(
            journal_vals
        )
        self.journal_purchase.write(
            journal_vals
        )

        terminal_00001 = self.Terminal.create({"name": "Terminal 1",
                                               "code": "00001",
                                               "location_id": self.env.ref("l10n_cr_invoice.sucursal_1").id})
        terminal_00001.action_confirm()
        self.terminal_id = terminal_00001

    def test_l10n_cr_out_invoice_document_without_p12_file(self):
        """Test prueba de Factura de cliente sin Llave Criptografica. """
        self._setup_company_cr_issuer()
        self.certificate.p12_file = None
        self.product_a.list_price = 250000.00
        form = self._l10n_cr_create_form_move(
            move_type="out_invoice",
            internal_type="out_invoice",
            partner=self.partner_taxpayer,
        )

        with self.assertRaises(UserError):
            invoice = form.save()
            invoice.action_post()

    def test_l10n_cr_invoice_type_voucher_type(self):
        """Test prueba q no podemos usar tipos de documentos debit_note o invoice en reembolsos de facturas."""
        self._setup_company_cr_issuer()
        self.product_a.list_price = 250000.00
        voucher_type_id = self.env.ref("l10n_cr_invoice.voucher_01")
        form = self._l10n_cr_create_form_move(
            move_type="out_refund",
            # internal_type="out_refund",
            partner=self.partner_taxpayer,
            voucher_type=voucher_type_id,
            terminal=self.terminal_id,
        )
        with self.assertRaises(ValidationError):
            invoice = form.save()
            invoice.action_post()

