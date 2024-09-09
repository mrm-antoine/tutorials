from odoo import models, Command, fields


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
            
        self.env['account.move'].create([
            {'partner_id': self.buyer_id.id,
             'move_type': 'out_invoice',
             'date': fields.Date.today(),
             'state': 'draft',
             'name': f'Invoice {self.name} n°{self.id}',
             'invoice_line_ids': [
                     Command.create(
                     {
                        'name': '6% of selling price',
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06             
                     }),
                     Command.create(
                     {
                        'name': 'administrative fees',
                         'quantity': 1,
                         'price_unit': 100
                     })
                ]
             }]
        ) 




        return super().action_sold()
    
    
    # Version TO

    # def action_sold(self):
    #     self.env["account.move"].create(
    #         [
    #             {
    #                 "name": "test",
    #                 "move_type": "out_invoice",
    #                 "partner_id": self.partner_id.id,
    #                 "line_ids": [
    #                     Command.create(
    #                         {
    #                             "price_unit": self.selling_price * (1 + 6 / 100)
    #                                           + 100.00,
    #                             "quantity": 1,
    #                         }
    #                     )
    #                 ],
    #             }
    #         ]
    #     )
    #     return super().action_sold()