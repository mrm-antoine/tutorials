from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate offer properties"
    _order = "price desc"

    _sql_constraints = [
        ('check_price', 'CHECK (price >= 0)', 'The price must be strictly positive'),
    ]

    price = fields.Float(string="Price")
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.context_today(record) + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            estate = record.property_id
            if estate.state == "canceled":
                raise UserError("You cannot accept offer on a canceled property.")
            if estate.state == "sold":
                raise UserError("You cannot accept offer on a sold property.")

            # Check if another offer is already accepted
            existing_accepted_offer = self.search([
                ('property_id', '=', estate.id),
                ('status', '=', 'accepted')
            ])
            if existing_accepted_offer:
                raise UserError("You cannot accept multiple offers on a single property.")
            estate.selling_price = record.price
            estate.buyer_id = record.partner_id.id
            record.status = "accepted"
        return True

    def action_refuse(self):
        for record in self:
            estate = record.property_id
            if estate.state == "canceled":
                raise UserError("You cannot reject offer on a canceled property.")
            if estate.state == "sold":
                raise UserError("You cannot reject offer on a sold property.")
            record.status = "refused"
        return True
