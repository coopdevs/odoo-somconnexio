#
from odoo import models, fields, api
from odoo.exceptions import UserError


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'
    share_product_id = fields.Many2one(required=False)
    type = fields.Selection(selection_add=[('referred', 'Referred')])

    referrer_id = fields.Many2one(
        'res.partner',
        string='Referrer',
        domain=[
            '|',
            ('cooperator', '=', True),
            ('member', '=', True),
        ]
    )

    @api.one
    def validate_subscription_request(self):
        try:
            invoice = super().validate_subscription_request()
        except UserError:
            if self.ordered_parts == 0 and self.type == 'referred':
                pass
            else:
                raise
        else:
            return invoice
        # TODO Implement refered case
        partner_obj = self.env['res.partner']

        partner = self.create_coop_partner()
        self.partner_id = partner

        partner.cooperator = False

        # TODO: Can we extract this piece of code to a new method?
        if self.is_company and not partner.has_representative():
            contact = False
            if self.email:
                domain = [('email', '=', self.email)]
                contact = partner_obj.search(domain)
                if contact:
                    contact.type = 'representative'
            if not contact:
                contact_vals = self.get_representative_vals()
                partner_obj.create(contact_vals)
            else:
                if len(contact) > 1:
                    raise UserError(_('There is two different persons with the'
                                      ' same national register number. Please'
                                      ' proceed to a merge before to continue')
                                    )
                if contact.parent_id and contact.parent_id.id != partner.id:
                    raise UserError(_('This contact person is already defined'
                                      ' for another company. Please select'
                                      ' another contact'))
                else:
                    contact.write({'parent_id': partner.id,
                                   'representative': True})

        self.write({'state': 'done'})
        return True

    def get_partner_company_vals(self):
        values = super().get_partner_company_vals()
        values['referrer_id'] = self.referrer_id.id
        return values

    def get_partner_vals(self):
        values = super().get_partner_company_vals()
        values['referrer_id'] = self.referrer_id.id
        return values
