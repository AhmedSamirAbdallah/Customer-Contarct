from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, time

class CustomerContract(models.Model):
    _name = "customer.contract"
    _rec_name = "customer"

    customer = fields.Many2one('res.partner', domain=[('is_customer', '=', True)])
    start_date = fields.Date("Start Date", default=fields.Date.today())
    end_date = fields.Date("End Date", default=fields.Date.today())
    price = fields.Float()
    avg_day_price = fields.Float("AVG Day Price", default=0, compute="_compute_avg_day_price")
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('ended', 'End'),
    ], string='state', required=True, readonly=True,
        default='draft')
    last_change = fields.Many2one('res.users', default=lambda self: self.env.user.id, readonly=True, )

    def get_current_user(self):
        current_user = self.env.uid
        return self.env['res.users'].browse(current_user).name

    def button_draft(self):
        for record in self:
            record.state = "draft"

    def button_confirmed(self):
        for record in self:
            record.state = "confirmed"

    def button_cancelled(self):
        for record in self:
            record.state = "cancelled"

    def button_ended(self):
        for record in self:
            record.state = "ended"

    @api.constrains('start_date', 'end_date')
    def check_valid_date(self):
        for record in self:
            if not record.start_date:
                raise ValidationError(
                    'start date can not be empty'
                )
            if not record.end_date:
                raise ValidationError(
                    'start date can not be empty'
                )
            if record.start_date >= record.end_date:
                raise ValidationError(
                    'Invalid Start Date and End Date '
                )

    @api.depends('start_date', 'end_date', 'price')
    def _compute_avg_day_price(self):
        for record in self:
            delta = record.end_date - record.start_date
            if delta:
                record.avg_day_price = record.price / delta.days

    def write(self, vals):
        if 'state' in vals.keys():
            for record in self:
                record.last_change = self.env.user.id
        return super(CustomerContract, self).write(vals)

    @api.model
    def change_end_date(self):
        for record in self.search([]):
            if record.end_date == date.today():
                record.state = "ended"
