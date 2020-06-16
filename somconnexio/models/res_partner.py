from odoo import models, fields, api


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
    coop_sponsee = fields.Boolean(string="Cooperator Sponsee",
                                    compute="_compute_coop_sponsee",
                                    store=True,
                                    readonly=True)

    @api.multi
    @api.depends("sponsor_id")
    @api.depends("subscription_request_ids.state")
    def _compute_coop_candidate(self):
        super()._compute_coop_candidate()
        for partner in self:
            if partner.sponsor_id:
                partner.coop_candidate = False
    @api.multi
    @api.depends("sponsor_id")
    def _compute_coop_sponsee(self):
        for partner in self:
            if partner.sponsor_id:
                partner.coop_sponsee = True
            else:
                partner.coop_sponsee = False