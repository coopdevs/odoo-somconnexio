from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class ProductCategoryTechnologySupplier(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.contract_adsl_args = {
            'name': 'contract w/service technology to adsl',
            'contract_category_id': self.ref('somconnexio.broadband'),
            'service_technology_id': self.ref(
                'somconnexio.service_technology_adsl'
            ),
            'partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'contract_line_ids': []
        }
        self.contract_mobile_args = {
            'name': 'contract w/category contract to mobile '
                    'and w/o service technology',
            'contract_category_id': self.ref('somconnexio.mobile'),
            'service_technology_id': self.ref(
                'somconnexio.service_technology_mobile'
            ),
            'partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'contract_line_ids': []
        }
        self.contract_fiber_args = {
            'name': 'contract w/service technology to fiber',
            'contract_category_id': self.ref('somconnexio.broadband'),
            'service_technology_id': self.ref(
                'somconnexio.service_technology_fiber'
            ),
            'partner_id': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'contract_line_ids': []
        }

        broadband_adsl_product_tmpl_args = {
            'name': 'ADSL 20Mb',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_adsl_service')
        }
        product_adsl_broadband_tmpl = self.env['product.template'].create(
            broadband_adsl_product_tmpl_args
        )
        self.product_broadband_adsl = product_adsl_broadband_tmpl.product_variant_id

        broadband_adsl_oneshot_product_tmpl_args = {
            'name': 'Alta parell existent a terminis',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_oneshot_adsl_service')
        }
        product_adsl_oneshot_tmpl = self.env['product.template'].create(
            broadband_adsl_oneshot_product_tmpl_args
        )
        self.product_broadband_adsl_oneshot = product_adsl_oneshot_tmpl.product_variant_id

        broadband_fiber_product_tmpl_args = {
            'name': 'Fiber',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_fiber_service')
        }
        product_broadband_fiber_tmpl = self.env['product.template'].create(
            broadband_fiber_product_tmpl_args
        )
        self.product_broadband_fiber = product_broadband_fiber_tmpl.product_variant_id

        broadband_oneshot_product_tmpl_args = {
            'name': 'Recollida router',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_oneshot_service')
        }
        product_oneshot_tmpl = self.env['product.template'].create(
            broadband_oneshot_product_tmpl_args
        )
        self.product_broadband_oneshot = product_oneshot_tmpl.product_variant_id

        mobile_product_tmpl_args = {
            'name': 'Sense minutes',
            'type': 'service',
            'categ_id': self.ref('somconnexio.mobile_service')
        }
        product_mobile_tmpl = self.env['product.template'].create(
            mobile_product_tmpl_args
        )
        self.product_mobile = product_mobile_tmpl.product_variant_id

        mobile_oneshot_product_tmpl_args = {
            'name': '1GB Addicional',
            'type': 'service',
            'categ_id': self.ref('somconnexio.mobile_service')
        }
        product_mobile_oneshot_tmpl = self.env['product.template'].create(
            mobile_oneshot_product_tmpl_args
        )
        self.product_mobile_oneshot = product_mobile_oneshot_tmpl.product_variant_id

    def test_contract_adsl_orage_wrong_product(self):
        contract_adsl_worng_product_args = self.contract_adsl_args.copy()
        contract_adsl_worng_product_args['contract_line_ids'] = [(0, False, {
            "name": "ADSL",
            "product_id": self.product_broadband_fiber.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_adsl_worng_product_args]
        )

    def test_contract_adsl_orage_allowed_product(self):
        contract_adsl_worng_product_args = self.contract_adsl_args.copy()
        contract_adsl_worng_product_args['contract_line_ids'] = [(0, False, {
            "name": "ADSL",
            "product_id": self.product_broadband_adsl.id
        })]
        self.assertTrue(
            self.env['contract.contract'].create(contract_adsl_worng_product_args)
        )
