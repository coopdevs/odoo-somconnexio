from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'

    iban = fields.Char(required=True)

    type = fields.Selection(
        selection_add=[(
            'sponsorship_coop_agreement',
            'Sponsorship Coop Agreement'
        )])

    coop_agreement_id = fields.Many2one(
        'coop.agreement',
        string='Coop Agreement'
    )

    def get_partner_company_vals(self):
        values = super().get_partner_company_vals()
        values['coop_agreement_id'] = self.coop_agreement_id and \
            self.coop_agreement_id.id

        return values

    def get_partner_vals(self):
        values = super().get_partner_vals()
        values['coop_agreement_id'] = self.coop_agreement_id and \
            self.coop_agreement_id.id

        return values

    @api.one
    def validate_subscription_request(self):
        try:
            invoice = super().validate_subscription_request()
        except UserError:
            if self.ordered_parts == 0 and self.type == 'sponsorship_coop_agreement':
                pass
            else:
                raise
        else:
            return invoice

        self.partner_obj = self.env['res.partner']

        self._check_already_cooperator()

        if not self.partner:
            self.partner = self.create_coop_partner()
            self.partner_id = self.partner
        else:
            self.partner = self.partner[0]

        self.partner.cooperator = True

        self._create_company_contact()

        self.write({'state': 'done'})
        return True

    @api.one
    @api.constrains('coop_agreement_id', 'type')
    def _check_coop_agreement_id(self):
        if self.type == 'sponsorship_coop_agreement' and not self.coop_agreement_id:
            raise ValidationError(
                "If it's a Coop Agreement sponsorship the Coop Agreement must be set."
            )
