from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    referenced_ids = fields.One2many(
        'subscription.request',
        'referrer_id',
        string='Referenced',
        readonly=True
    )

    referrer_id = fields.Many2one(
        'res.partner',
        string='Referrer',
        domain=[
            '|',
            ('cooperator', '=', True),
            ('member', '=', True),
        ]
    )
