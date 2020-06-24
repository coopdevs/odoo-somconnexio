from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_subscription_request = fields.Many2one(
        'subscription.request',
        string='Last subscription request',
        compute='_compute_last_subscription_request',
    )
    
    @api.multi
    def _compute_last_subscription_request(self):
        request_obj = self.env['subscription.request']
        for partner in self:
            request = request_obj.search([
                ('partner_id','=',partner.id)
            ],order='id DESC', limit=1)
            self.last_subscription_request = request
