from odoo import models, fields


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'
    iban = fields.Char(required=True)
