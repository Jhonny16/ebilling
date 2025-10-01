# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
L10N_CR_DESCRIPTION_DISCOUNT_TYPE_CODE = [
    ('01', 'Descuento por Regalía'),
    ('02', 'Descuento por Regalía IVA Cobrado al Cliente'),
    ('03', 'Descuento por Bonificación'),
    ('04', 'Descuento por volumen'),
    ('05', 'Descuento por Temporada (estacional)'),
    ('06', 'Descuento promocional'),
    ('07', 'Descuento Comercial'),
    ('08', 'Descuento por frecuencia'),
    ('09', 'Descuento sostenido'),
    ('10', 'Otros descuentos'),
]


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    l10n_cr_discount_type_code = fields.Selection(selection=L10N_CR_DESCRIPTION_DISCOUNT_TYPE_CODE,
                                                  string="Discount Type Code", help="NOTA 20: ANEXOS y ESTRCUTURAS")
    l10n_cr_has_exoneration = fields.Boolean(compute="_compute_l10n_cr_has_exoneration", string="Has Exoneration")

    @api.depends('move_id.partner_id', 'product_id')
    def _compute_l10n_cr_has_exoneration(self):
        for line in self:
            line.l10n_cr_has_exoneration = False
            product_id = line.product_id
            if line.move_id.partner_id.l10n_cr_exoneration_authorization and line.product_id and product_id.product_cabys_id:
                allowed_cabys = line.partner_id.l10n_cr_allowed_cabys_ids
                if allowed_cabys.filtered(lambda x: x.exoneration_code and x.exoneration_code in product_id.product_cabys_id.code):
                    line.l10n_cr_has_exoneration = True

    # extends
    def _get_computed_taxes(self):
        if self.move_id.l10n_cr_has_exoneration and self.move_id.fiscal_position_id and self.move_id.country_code == 'CR' and self.move_id.l10n_cr_fiscal_journal:
            self.ensure_one()

            company_domain = self.env['account.tax']._check_company_domain(self.move_id.company_id)
            if self.move_id.is_sale_document(include_receipts=True):
                # Out invoice.
                filtered_taxes_id = self.product_id.taxes_id.filtered_domain(company_domain)
                tax_ids = filtered_taxes_id or self.account_id.tax_ids.filtered(lambda tax: tax.type_tax_use == 'sale')

            elif self.move_id.is_purchase_document(include_receipts=True):
                # In invoice.
                filtered_supplier_taxes_id = self.product_id.supplier_taxes_id.filtered_domain(company_domain)
                tax_ids = filtered_supplier_taxes_id or self.account_id.tax_ids.filtered(lambda tax: tax.type_tax_use == 'purchase')

            else:
                tax_ids = False if self.env.context.get('skip_computed_taxes') else self.account_id.tax_ids

            if self.company_id and tax_ids:
                tax_ids = tax_ids._filter_taxes_by_company(self.company_id)

            if tax_ids and self.move_id.fiscal_position_id and self.l10n_cr_has_exoneration:
                tax_ids = self.move_id.fiscal_position_id.map_tax(tax_ids)

            return tax_ids
        else:
            return super()._get_computed_taxes()
