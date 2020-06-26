from odoo import models, fields


class Contract(models.Model):
    _inherit = 'contract.contract'

    contract_category_id = fields.Many2one(
        'contract.category',
        'Category Contract'
    )
