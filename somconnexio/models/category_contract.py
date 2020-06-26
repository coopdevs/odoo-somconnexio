from odoo import models, fields


class CategoryContract(models.Model):
    _name = "contract.category"
    name = fields.Char('Category name')


class CategoryContractProduct(models.Model):
    _name = "contract.category.product"
    contract_category = fields.Many2one('contract.category')
    product_category = fields.Many2one('product.category')
