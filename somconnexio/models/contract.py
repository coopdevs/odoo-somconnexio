from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = 'contract.contract'

    contract_category_id = fields.Many2one(
        'contract.category',
        'Category Contract'
    )

    @api.one
    @api.constrains('contract_category_id', 'contract_line_ids')
    def _check_contract_category_products(self):
        available_relations = self.env['contract.category.product'].search([
            ('contract_category', '=', self.contract_category_id.id)
        ])
        available_categories = [c.product_category.id for c in available_relations]
        available_products_categ = self.env['product.template'].search([
            ('categ_id', 'in', available_categories)
        ])

        for line in self.contract_line_ids:
            if (line.product_id.product_tmpl_id not in available_products_categ):
                raise ValidationError(
                    'Product %s is not allowed by contract type %s' % (
                        line.product_id.name, self.contract_category_id.name
                    )
                )
