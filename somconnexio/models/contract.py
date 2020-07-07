from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = 'contract.contract'

    contract_category_id = fields.Many2one(
        'contract.category',
        'Category Contract',
        required = True
    )
    service_technology_id = fields.Many2one(
        'service.technology',
        'Service Technology'
    )

    @api.one
    @api.constrains('contract_category_id', 'service_technology_id')
    def _check_contract_category_service_technology(self):
        available_relations = (
            self.env['contract.category.service.technology'].search([
                ('contract_category_id', '=', self.contract_category_id.id)
            ])
        )
        available_services_tech = [
            c.service_technology_id.id for c in available_relations
        ]
        if self.service_technology_id.id not in available_services_tech:
            raise ValidationError(
                'Service technology %s is not allowed by contract type %s' % (
                    self.service_technology_id.name,
                    self.contract_category_id.name
                )
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
            if line.product_id.product_tmpl_id not in available_products_categ:
                raise ValidationError(
                    'Product %s is not allowed by contract type %s' % (
                        line.product_id.name, self.contract_category_id.name
                    )
                )

    @api.one
    @api.constrains('partner_id', 'contract_line_ids')
    def _check_coop_agreement(self):
        if self.partner_id.coop_agreement:
            for line in self.contract_line_ids:
                line_prod_tmpl_id = line.product_id.product_tmpl_id
                agreement = self.partner_id.coop_agreement_id
                if line_prod_tmpl_id not in agreement.products:
                    raise ValidationError(
                        'Product %s is not allowed by agreement %s' % (
                            line.product_id.name, agreement.code
                        )
                    )

    @api.model
    def create(self, values):
        if 'service_technology_id' not in values:
            mobile_category_id = self.env.ref('somconnexio.mobile').id
            if values['contract_category_id'] == mobile_category_id:
                values['service_technology_id'] = self.env.ref(
                    'somconnexio.service_technology_mobile'
                ).id
        res = super(Contract, self).create(values)
        return res