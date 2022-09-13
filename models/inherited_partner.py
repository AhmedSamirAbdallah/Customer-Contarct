from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Partner(models.Model):
    _inherit = "res.partner"

    is_customer = fields.Boolean("Is Customer")
    total_contracts_price = fields.Integer("Total Contracts Price", readonly=True, default=0,
                                           compute="_compute_total_contract",
                                           store=True)
    customer_contract_id = fields.One2many('customer.contract', 'customer')

    @api.depends('customer_contract_id', 'customer_contract_id.state', 'customer_contract_id.price')
    def _compute_total_contract(self):
        for record in self:
            record.total_contracts_price = 0
            total_price = self.env['customer.contract'].search(
                [('state', '=', 'confirmed'), ('customer', '=', record.id)])
            for total in total_price:
                record.total_contracts_price += total.price
