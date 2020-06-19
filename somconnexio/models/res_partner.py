
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    coop_agreement_id = fields.Many2one(
        'coop.agreement',
        string='Coop Agreement'
    )
