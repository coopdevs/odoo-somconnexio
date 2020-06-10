from odoo import models, fields


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'
    type = fields.Selection(selection_add=[('refered','Refered')])
