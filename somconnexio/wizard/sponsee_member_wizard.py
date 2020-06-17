from odoo import api, exceptions, fields, models
from datetime import datetime

class SubscriptionUpgradeSponsee(models.TransientModel):
    _name = 'subscription.upgrade.sponsee'
    _description = 'Change a partner from sponsee to member'
    partner_id = fields.Many2one('res.partner')
    share_product_id = fields.Many2one('product.product',
                                       string='Share type',
                                       domain=[('is_share', '=', True)],
                                       required=True)
    ordered_parts = fields.Integer(string='Number of Share',
                                   required=True,
                                   default=1)

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        defaults['partner_id'] = self.env.context['active_id']
        return defaults

    @api.multi
    def button_upgrade(self):
        self.ensure_one()
        request_obj = self.env['subscription.request']
        vals_subscription = {
            'already_cooperator': True,
            'partner_id': self.partner_id.id,
            'ordered_parts': self.ordered_parts,
            'date': datetime.now(),
            'source': 'manual',
            'share_product_id': self.share_product_id.id,
            'firstname': self.partner_id.firstname,
            'name': self.partner_id.name,
            'lastname': self.partner_id.lastname,
            'email': self.partner_id.email,
            'birthdate': self.partner_id.birthdate_date,
            'gender': self.partner_id.gender,
            'address': self.partner_id.street,
            'city': self.partner_id.city,
            'zip_code': self.partner_id.zip,
            'country_id': self.partner_id.country_id.id,
            'phone': self.partner_id.phone,
            'lang': self.partner_id.lang,

        }
        subscription = request_obj.create(vals_subscription)
        subscription.validate_subscription_request()
        self.partner_id.sponsor_id = False
        return True