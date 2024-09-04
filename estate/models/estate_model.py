from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties"

    name = fields.Char(string='Title', required=True)
    description =  fields.Text()
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string="Available From" ,default=lambda self:(fields.Datetime.now() + relativedelta(months=3)), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='',
        selection=[("north", "North"),("south", "South"),("east", "East"),("west", "West")],
    )
    active = fields.Boolean(string='Active')
    state = fields.Selection(string='Status', selection=[("new", "New"),("offer_received", "Offer Received"), ("sold", "Sold"), ("canceled", "Canceled")], default="new")
