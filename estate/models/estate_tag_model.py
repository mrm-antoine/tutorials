from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate tag properties"
    _order = "name"

    _sql_constraints = [
        ('check_unique_tag', 'UNIQUE(name)', 'Name must be unique')
    ]
    
    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
