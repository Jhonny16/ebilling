# -*- coding: utf-8 -*-
from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cr', 'account.tax')
    def _get_cr_edi_account_tax(self):
        return self._parse_csv('cr', 'account.tax', module='l10n_cr_invoice')

    @template('cr', 'account.tax.group')
    def _get_cr_edi_account_tax_group(self):
        return self._parse_csv('cr', 'account.tax.group', module='l10n_cr_invoice')

    @template('cr', 'account.journal')
    def _get_cr_account_journal(self):
        return {
            "tareta_journal": {
                'type': 'bank',
                'name': 'Tarjeta',
                'code': 'TC',
            },
            "cheque_journal": {
                'type': 'bank',
                'name': 'Cheque',
                'code': 'CH',
            },
            "transferencia_journal": {
                'type': 'bank',
                'name': 'Transferencia - depósito bancario',
                'code': 'T-DB',
            },
            "terceros_journal": {
                'type': 'cash',
                'name': 'Recaudado por terceros',
                'code': 'RT',
            },
        }
