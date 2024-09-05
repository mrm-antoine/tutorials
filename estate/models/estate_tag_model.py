from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate tag properties"

    name = fields.Char(string="Name", required=True)
    
    _sql_constraints = [
        ('check_unique_tag', 'UNIQUE(name)', 'Name must be unique')
    ]