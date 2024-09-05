from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate properties"

    _sql_constraints = [
        ('check_expected_price', 'CHECK (expected_price > 0)','The expected_price must be strictly positive'),
        ('check_selling_price', 'CHECK (selling_price >= 0)','The selling_price must be positive'),
    ]

    name = fields.Char(string='Title', required=True)
    description =  fields.Text()
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string="Available From" ,default=lambda self:(fields.Datetime.now() + relativedelta(months=3)), copy=False)
    expected_price = fields.Float(required=True)
    # expected_price = fields.Float(required=True, domain=[('expected_price', '>', 0)])
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
    best_price = fields.Float(compute="_compute_best_price", string='Best Price')

    


    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(of_rec.price for of_rec in record.offer_ids)
            else:
                record.best_price = 0
        #  optimisation req
        # res = self.env["estate.property.offer"].read_group(domain=[("property_id", "in", self.ids)], groupby="property_id", fields=["price:max"])
        # map_zzz = {elt["property_id"][0]: elt["price"] for elt in res}
        # for record in self:
        #     record.best_price = map_zzz.get(record.id, 0) # max(of_rec.price for of_rec in record.offer_ids)

        # [ val for val in sequence if cond ]              # sequence : List[Any]                List
        # { key: val for key, val in sequence if cond }    # sequence : List[Tuple(Any, Any)]    Dict
        # { val for val in sequence if cond }              # sequence : List[Any]                Set

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None
            
            
    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")    
            record.state = "sold"
        return True
    
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancel.")    
            record.state = "canceled"
        return True
    
    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.offer_ids and  float_compare(record.selling_price, record.expected_price * 0.90, precision_digits=2) < 0:
                raise UserError("Selling price must be at least 90% of the expected price.")
        