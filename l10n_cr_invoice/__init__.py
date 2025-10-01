# -*- coding: utf-8 -*-

from . import models
from . import wizard


def _l10n_cr_edi_post_init(env):
    for company in env['res.company'].search([('chart_template', '=', 'cr')]):
        Template = env['account.chart.template'].with_company(company)
        Template._load_data({'account.tax.group': Template._get_cr_edi_account_tax_group()})
        Template._load_data({'account.tax': Template._get_cr_edi_account_tax()})
