from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate type properties"

    name = fields.Char(string="Name", required=True)

