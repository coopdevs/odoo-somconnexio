#
from odoo import models, fields, api
from odoo.exceptions import UserError


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'
    share_product_id = fields.Many2one(required=False)
    type = fields.Selection(selection_add=[('referred', 'Referred')])

    @api.one
    def validate_subscription_request(self):
        try:
            invoice = super().validate_subscription_request()
        except UserError:
            if self.ordered_parts == 0 and self.type == 'referred':
                pass
                raise # Not implemented yet
            else:
                raise
        else:
            return invoice
        # TODO Implement refered case
