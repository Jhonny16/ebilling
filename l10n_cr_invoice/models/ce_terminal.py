# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning


class CRTerminal(models.Model):
    _name = "ce.terminal"
    _description = "Terminal o punto de venta que pertenece a una Sucursal"
    _sql_constraints = [
        ('code_uniq', 'unique(code, company_id, location_id)', 'Código único por Sucursal y Compañia!'),
    ]

    name = fields.Char(string="Terminal", required=True, copy=False)
    code = fields.Char(required=True, size=5, copy=False, help='00001 for the first terminal')
    location_id = fields.Many2one('ce.location', string='Sucursal', required=True, copy=False)
    company_id = fields.Many2one('res.company', string="Compañia", readonly=True,
                                 default=lambda self: self.env.company)
    economic_activity_id = fields.Many2one("ce.economic.activity", "Economic Activity",
                                           help="Dejar en blanco para facturar por la actividad principal de la compañía.")
    l10n_cr_available_economic_activities_ids = fields.Many2many('ce.economic.activity',
                                                                 compute='_compute_l10n_cr_available_economic_activities')
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        copy=False,
    )

    # Tipos de secuencia para las facturas
    sequence_fe = fields.Many2one('ir.sequence', string="Factura electrónica")
    sequence_nd = fields.Many2one('ir.sequence', string="Nota de débito electrónica")
    sequence_nc = fields.Many2one('ir.sequence', string="Nota de crédito electrónica")
    sequence_te = fields.Many2one('ir.sequence', string="Tiquete Electrónico")
    sequence_cace = fields.Many2one('ir.sequence', string="Confirmación de aceptación del comprobante electrónico")
    sequence_capce = fields.Many2one('ir.sequence',
                                     string="Confirmación de aceptación parcial del comprobante electrónico")
    sequence_crce = fields.Many2one('ir.sequence', string="Confirmación de rechazo del comprobante electrónico")
    sequence_fec = fields.Many2one('ir.sequence', string="Factura electrónica de compra")
    sequence_fee = fields.Many2one('ir.sequence', string="Factura electrónica de exportación")
    sequence_rep = fields.Many2one('ir.sequence', string="Recibo Electronico de Pago")

    # === COMPUTE METHODS ===#

    @api.depends('company_id')
    def _compute_l10n_cr_available_economic_activities(self):
        self.l10n_cr_available_economic_activities_ids = False
        for rec in self:
            rec.l10n_cr_available_economic_activities_ids = self.env['ce.economic.activity'].search(
                rec._get_l10n_cr_economic_activities_domain())

    # ===== BUTTONS =====

    def action_confirm(self):
        for rec in self:
            rec._validate_vat()
            location = self.env['ce.location'].browse(rec.location_id.id)
            vals = {'code': rec.code}
            terminal_vals = {
                "sequence_fe": self._create_sequence(name="Factura electrónica", code="01", pref="fe",
                                                     vals=vals, location=location).id,
                "sequence_nd": self._create_sequence(name="Nota de débito electrónica", code="02",
                                                     pref="nd", vals=vals, location=location).id,
                "sequence_nc": self._create_sequence(name="Nota de crédito electrónica", code="03",
                                                     pref="nc", vals=vals, location=location).id,
                "sequence_te": self._create_sequence(name="Tiquete Electrónico", code="04",
                                                     pref="te", vals=vals, location=location).id,
                "sequence_cace": self._create_sequence(name="Confirmación de aceptación del comprobante electrónico",
                                                       code="05", pref="cace", vals=vals, location=location).id,
                "sequence_capce": self._create_sequence(name="Confirmación de aceptación parcial del comprobante electrónico",
                                                        code="06", pref="capce", vals=vals, location=location).id,
                "sequence_crce": self._create_sequence(name="Confirmación de rechazo del comprobante electrónico",
                                                       code="07", pref="crce", vals=vals, location=location).id,
                "sequence_fec": self._create_sequence(name="Factura electrónica de compra", code="08",
                                                      pref="fec", vals=vals, location=location).id,
                "sequence_fee": self._create_sequence(name="Factura electrónica de exportación", code="09",
                                                      pref="fee", vals=vals, location=location).id,
                "sequence_rep": self._create_sequence(name="Recibo Electronico de Pago", code="10",
                                                      pref="rep", vals=vals, location=location).id,
                "state": 'active',
            }
            rec.write(terminal_vals)

    def action_cancel(self):
        self.ensure_one()
        msg = _(
            "Are you sure want to cancel this Terminal? " "Once you cancel this Terminal cannot be used."
        )
        action = self.env.ref("l10n_cr_invoice.l10n_cr_terminal_validate_wizard_action").read()[0]
        action["context"] = {
            "default_name": msg,
            "default_terminal_id": self.id,
            "action": "cancel",
        }
        return action

    # === BUSINESS METHODS ===#

    def _get_l10n_cr_economic_activities_domain(self):
        self.ensure_one()
        company_id = self.company_id
        domain = [('id', 'in', company_id.l10n_cr_economic_activity_ids.ids)]
        return domain

    def _validate_vat(self):
        if not self.company_id.vat:
            action = self.env.ref("base.action_res_company_form")
            msg = _("Company does not have a VAT defined")
            raise RedirectWarning(msg, action.id, _("Go to Companies"))

    @api.model
    def _get_sequence_code(self, code, pref, vals, location):
        return "%s_%s_%s_%s" % (pref, location.code, vals['code'], code)

    @api.model
    def _create_sequence(self, name=None, code=None, pref=None, vals={}, location=None):
        code = self._get_sequence_code(code, pref, vals, location)
        seq = {
            'name': name or 'Sequence',
            'code': code,
            'implementation': 'no_gap',
            'padding': 10,
            'number_next': 1,
            'number_increment': 1,
            'use_date_range': False,
            'company_id': self.company_id.id,
        }
        seq = self.env['ir.sequence'].create(seq)
        return seq

    def _action_cancel(self):
        for rec in self:
            rec.state = "cancelled"
            if rec.sequence_fe:
                rec.sequence_fe.active = False
            if rec.sequence_nd:
                rec.sequence_nd.active = False
            if rec.sequence_nc:
                rec.sequence_nc.active = False
            if rec.sequence_te:
                rec.sequence_te.active = False
            if rec.sequence_cace:
                rec.sequence_cace.active = False
            if rec.sequence_capce:
                rec.sequence_capce.active = False
            if rec.sequence_crce:
                rec.sequence_crce.active = False
            if rec.sequence_fec:
                rec.sequence_fec.active = False
            if rec.sequence_fee:
                rec.sequence_fee.active = False
            if rec.sequence_rep:
                rec.sequence_rep.active = False

    def action_view_sequence(self):
        self.ensure_one()
        action = self.env.ref("base.ir_sequence_form").read()[0]
        domain = [self.sequence_fe.id, self.sequence_nd.id, self.sequence_nc.id, self.sequence_te.id,
                  self.sequence_fec.id, self.sequence_fee.id, self.sequence_cace.id, self.sequence_capce.id,
                  self.sequence_crce.id, self.sequence_rep.id]
        if domain:
            action["views"] = [(self.env.ref("base.sequence_view_tree").id, "list"),
                               (self.env.ref("base.sequence_view").id, "form")]
            action["domain"] = [('id', 'in', domain)]
        else:
            action = {"type": "ir.actions.act_window_close"}

        return action

    # def gen_numeracion_consecutiva(self, voucher_type_id):
    def gen_consecutive_number(self, voucher_type_id):
        sequence = {
            '01': self.sequence_fe,
            '02': self.sequence_nd,
            '03': self.sequence_nc,
            '04': self.sequence_te,
            '05': self.sequence_cace,
            '06': self.sequence_capce,
            '07': self.sequence_crce,
            '08': self.sequence_fec,
            '09': self.sequence_fee,
            '10': self.sequence_rep,
        }
        if voucher_type_id.code in sequence:
            seq = sequence[voucher_type_id.code]
            if not seq:
                raise UserError(_("The voucher type has no defined sequence."))

        try:
            consecutive = "%s%s%s%s" % (
                self.location_id.code,
                self.code,
                voucher_type_id.code,
                sequence[voucher_type_id.code].next_by_id())
        except Exception as e:
            raise UserError(_("Error getting consecutive numbering: \n %s") % e)
        return consecutive
