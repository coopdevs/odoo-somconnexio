from odoo import models, fields


class ContractCategory(models.Model):
    _name = "contract.category"
    name = fields.Char('Category name')


class ContractCategoryProduct(models.Model):
    _name = "contract.category.product"
    contract_category = fields.Many2one('contract.category')
    product_category = fields.Many2one('product.category')
