from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    coop_agreement_id = fields.Many2one(
        'coop.agreement',
        string='Coop Agreement'
    )
    coop_agreement = fields.Boolean(string="Has cooperator agreement?",
                                    compute="_compute_coop_agreement",
                                    store=True,
                                    readonly=True)

    @api.multi
    @api.depends("sponsor_id", "coop_agreement_id")
    @api.depends("subscription_request_ids.state")
    def _compute_coop_candidate(self):
        for partner in self:
            if partner.member:
                is_candidate = False
            else:
                sub_requests = partner.subscription_request_ids.filtered(
                    lambda record: (
                            record.state == 'done' and
                            not record.sponsor_id and
                            not record.coop_agreement_id
                    )
                )
                is_candidate = bool(sub_requests)
            partner.coop_candidate = is_candidate

    @api.multi
    @api.depends("sponsor_id", "coop_agreement_id")
    def _compute_coop_agreement(self):
        for partner in self:
            if partner.coop_agreement_id:
                partner.coop_agreement = True
            else:
                partner.coop_agreement = False
