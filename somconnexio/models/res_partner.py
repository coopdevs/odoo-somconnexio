from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sponsee_ids = fields.One2many(
        'subscription.request',
        'sponsor_id',
        string='Sponsees',
        readonly=True
    )

    sponsor_id = fields.Many2one(
        'res.partner',
        string='Sponsor',
        domain=[
            ('member', '=', True),
        ]
    )
