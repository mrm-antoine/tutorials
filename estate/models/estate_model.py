from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate properties"

    name = fields.Char(string='Title', required=True)
    description =  fields.Text()
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string="Available From" ,default=lambda self:(fields.Datetime.now() + relativedelta(months=3)), copy=False)
    expected_price = fields.Float(required=True, domain=[('expected_price', '>=', 0)])
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[("north", "North"),("south", "South"),("east", "East"),("west", "West")],
    )
    active = fields.Boolean(string='Active')
    state = fields.Selection(string='Status', selection=[("new", "New"),("offer_received", "Offer Received"), ("sold", "Sold"), ("canceled", "Canceled")], default="new")
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(compute="_compute_total_area",string='Total Area')
    # best_price = fields.

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area