from odoo import models, fields


class ServiceTechnology(models.Model):
    _name = 'service.technology'
    name = fields.Char('Name')


class ContractCategoryServiceTechnology(models.Model):
    _name = 'contract.category.service.technology'
    service_technology_id = fields.Many2one(
        'service.technology', 'Service Technology'
    )
    contract_category_id = fields.Many2one(
        'contract.category', 'Contract Category'
    )
