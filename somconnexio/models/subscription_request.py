from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'

    iban = fields.Char(required=True)

    type = fields.Selection(selection_add=[('sponsorship_coop_agreement', 'Sponsorship Coop Agreement')])

    coop_agreement_id = fields.Many2one(
        'coop.agreement',
        string='Coop Agreement'
    )

    @api.one
    @api.constrains('coop_agreement_id', 'type')
    def _check_coop_agreement_id(self):
        if self.type == 'sponsorship_coop_agreement' and not self.coop_agreement_id:
            raise ValidationError("If it's a Coop Agreement sponsorship the Coop Agreement must be set.")
