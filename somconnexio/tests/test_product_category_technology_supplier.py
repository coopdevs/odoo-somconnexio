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
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_masmovil'
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

        mobile_additional_product_tmpl_args = {
            'name': 'Internacional 100 Min',
            'type': 'service',
            'categ_id': self.ref('somconnexio.mobile_additional_service')
        }
        mobile_additional_product_tmpl = self.env['product.template'].create(
            mobile_additional_product_tmpl_args
        )
        self.product_mobile_additional = (
            mobile_additional_product_tmpl.product_variant_id
        )

        broadband_additional_product_tmpl_args = {
            'name': 'IPv4 Fixa',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_additional_service')
        }
        broadband_additional_product_tmpl = self.env['product.template'].create(
            broadband_additional_product_tmpl_args
        )
        self.product_broadband_additional = (
            broadband_additional_product_tmpl.product_variant_id
        )

    def test_contract_adsl_orange_wrong_product(self):
        contract_adsl_wrong_product_args = self.contract_adsl_args.copy()
        contract_adsl_wrong_product_args['contract_line_ids'] = [(0, False, {
            "name": "Fiber",
            "product_id": self.product_broadband_fiber.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_adsl_wrong_product_args]
        )

    def test_contract_adsl_orange_wrong_technology(self):
        contract_adsl_wrong_tech_args = self.contract_adsl_args.copy()
        contract_adsl_wrong_tech_args['service_technology_id'] = (
            self.ref("somconnexio.service_technology_fiber")
        )
        contract_adsl_wrong_tech_args['contract_line_ids'] = [(0, False, {
            "name": "ADSL",
            "product_id": self.product_broadband_adsl.id
        }), (0, False, {
            "name": "Alta parell existent a terminis",
            "product_id": self.product_broadband_adsl_oneshot.id
        }), (0, False, {
            "name": "IPv4 Fixa",
            "product_id": self.product_broadband_additional.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_adsl_wrong_tech_args]
        )

    def test_contract_adsl_orange_wrong_supplier(self):
        contract_adsl_wrong_supplier_args = self.contract_adsl_args.copy()
        contract_adsl_wrong_supplier_args['service_supplier_id'] = (
            self.ref("somconnexio.service_supplier_vodafone")
        )
        contract_adsl_wrong_supplier_args['contract_line_ids'] = [(0, False, {
            "name": "ADSL",
            "product_id": self.product_broadband_adsl.id
        }), (0, False, {
            "name": "Alta parell existent a terminis",
            "product_id": self.product_broadband_adsl_oneshot.id
        }), (0, False, {
            "name": "IPv4 Fixa",
            "product_id": self.product_broadband_additional.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_adsl_wrong_supplier_args]
        )


    def test_contract_adsl_orange_allowed_product(self):
        contract_adsl_allowed_product_args = self.contract_adsl_args.copy()
        contract_adsl_allowed_product_args['contract_line_ids'] = [(0, False, {
            "name": "ADSL",
            "product_id": self.product_broadband_adsl.id
        }), (0, False, {
            "name": "Alta parell existent a terminis",
            "product_id": self.product_broadband_adsl_oneshot.id
        }), (0, False, {
            "name": "IPv4 Fixa",
            "product_id": self.product_broadband_additional.id
        })]
        self.assertTrue(
            self.env['contract.contract'].create(contract_adsl_allowed_product_args)
        )

    def test_contract_mobile_wrong_product(self):
        contract_mobile_wrong_product_args = self.contract_mobile_args.copy()
        contract_mobile_wrong_product_args['contract_line_ids'] = [(0, False, {
            "name": "ADSL 20Mb",
            "product_id": self.product_broadband_adsl.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_mobile_wrong_product_args]
        )

    def test_contract_mobile_allowed_product(self):
        contract_mobile_allowed_product_args = self.contract_mobile_args.copy()
        contract_mobile_allowed_product_args['contract_line_ids'] = [(0, False, {
            "name": "Mobile Sense Minuts",
            "product_id": self.product_mobile.id
        }), (0, False, {
            "name": "One Shot Mobile",
            "product_id": self.product_mobile_oneshot.id
        }), (0, False, {
            "name": "Internacional 100 Min",
            "product_id": self.product_mobile_additional.id
        })]
        self.assertTrue(self.env['contract.contract'].create(
            contract_mobile_allowed_product_args
        ))

    def test_contract_mobile_wrong_technology(self):
        contract_mobile_wrong_tech_args = self.contract_mobile_args.copy()
        contract_mobile_wrong_tech_args['service_technology_id'] = (
            self.ref("somconnexio.service_technology_adsl")
        )
        contract_mobile_wrong_tech_args['contract_line_ids'] = [(0, False, {
            "name": "Mobile Sense Minuts",
            "product_id": self.product_mobile.id
        }), (0, False, {
            "name": "One Shot Mobile",
            "product_id": self.product_mobile_oneshot.id
        }), (0, False, {
            "name": "Internacional 100 Min",
            "product_id": self.product_mobile_additional.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_mobile_wrong_tech_args]
        )

    def test_contract_mobile_wrong_supplier(self):
        contract_mobile_wrong_supplier_args = self.contract_mobile_args.copy()
        contract_mobile_wrong_supplier_args['service_supplier_id'] = (
            self.ref("somconnexio.service_supplier_orange")
        )
        contract_mobile_wrong_supplier_args['contract_line_ids'] = [(0, False, {
            "name": "Mobile Sense Minuts",
            "product_id": self.product_mobile.id
        }), (0, False, {
            "name": "One Shot Mobile",
            "product_id": self.product_mobile_oneshot.id
        }), (0, False, {
            "name": "Internacional 100 Min",
            "product_id": self.product_mobile_additional.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_mobile_wrong_supplier_args]
        )

    def test_contract_fiber_orange_wrong_tech_product(self):
        contract_fiber_wrong_tech_args = self.contract_fiber_args.copy()
        contract_fiber_wrong_tech_args['service_supplier_id'] = self.ref(
            'somconnexio.service_supplier_orange'
        )
        contract_fiber_wrong_tech_args['service_technology_id'] = self.ref(
            'somconnexio.service_technology_adsl'
        )
        contract_fiber_wrong_tech_args['contract_line_ids'] = [(0, False, {
            "name": "Fiber",
            "product_id": self.product_broadband_fiber.id
        }), (0, False, {
            "name": "One Shot Broadband",
            "product_id": self.product_broadband_oneshot.id
        }), (0, False, {
            "name": "IPv4 Fixa",
            "product_id": self.product_broadband_additional.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_fiber_wrong_tech_args]
        )

    def test_contract_fiber_orange_allowed_product(self):
        contract_fiber_allowed_product_args = self.contract_fiber_args.copy()
        contract_fiber_allowed_product_args['service_supplier_id'] = self.ref(
            'somconnexio.service_supplier_orange'
        )
        contract_fiber_allowed_product_args['contract_line_ids'] = [(0, False, {
            "name": "Fiber",
            "product_id": self.product_broadband_fiber.id
        }), (0, False, {
            "name": "One Shot Broadband",
            "product_id": self.product_broadband_oneshot.id
        }), (0, False, {
            "name": "IPv4 Fixa",
            "product_id": self.product_broadband_additional.id
        })]
        self.assertTrue(
            self.env['contract.contract'].create(contract_fiber_allowed_product_args)
        )

    def test_contract_fiber_orange_wrong_product(self):
        contract_fiber_wrong_product_args = self.contract_fiber_args.copy()
        contract_fiber_wrong_product_args['service_supplier_id'] = self.ref(
            'somconnexio.service_supplier_orange'
        )
        contract_fiber_wrong_product_args['contract_line_ids'] = [(0, False, {
            "name": "ADSL 20Mb",
            "product_id": self.product_broadband_adsl.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_fiber_wrong_product_args]
        )

    def test_contract_fiber_vodafone_wrong_tech_product(self):
        contract_fiber_wrong_tech_args = self.contract_fiber_args.copy()
        contract_fiber_wrong_tech_args['service_technology_id'] = self.ref(
            'somconnexio.service_technology_adsl'
        )
        contract_fiber_wrong_tech_args['service_supplier_id'] = self.ref(
            'somconnexio.service_supplier_vodafone'
        )
        contract_fiber_wrong_tech_args['contract_line_ids'] = [(0, False, {
            "name": "Fiber",
            "product_id": self.product_broadband_fiber.id
        }), (0, False, {
            "name": "One Shot Broadband",
            "product_id": self.product_broadband_oneshot.id
        }), (0, False, {
            "name": "IPv4 Fixa",
            "product_id": self.product_broadband_additional.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_fiber_wrong_tech_args]
        )

    def test_contract_fiber_wrong_supplier(self):
        contract_fiber_wrong_supplier_args = self.contract_fiber_args.copy()
        contract_fiber_wrong_supplier_args['service_supplier_id'] = self.ref(
            'somconnexio.service_supplier_masmovil'
        )
        contract_fiber_wrong_supplier_args['contract_line_ids'] = [(0, False, {
            "name": "Fiber",
            "product_id": self.product_broadband_fiber.id
        }), (0, False, {
            "name": "One Shot Broadband",
            "product_id": self.product_broadband_oneshot.id
        }), (0, False, {
            "name": "IPv4 Fixa",
            "product_id": self.product_broadband_additional.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_fiber_wrong_supplier_args]
        )

    def test_contract_fiber_vodafone_allowed_product(self):
        contract_fiber_allowed_product_args = self.contract_fiber_args.copy()
        contract_fiber_allowed_product_args['service_supplier_id'] = self.ref(
            'somconnexio.service_supplier_vodafone'
        )
        contract_fiber_allowed_product_args['contract_line_ids'] = [(0, False, {
            "name": "Fiber",
            "product_id": self.product_broadband_fiber.id
        }), (0, False, {
            "name": "One Shot Broadband",
            "product_id": self.product_broadband_oneshot.id
        }), (0, False, {
            "name": "IPv4 Fixa",
            "product_id": self.product_broadband_additional.id
        })]
        self.assertTrue(
            self.env['contract.contract'].create(contract_fiber_allowed_product_args)
        )

    def test_contract_fiber_vodafone_wrong_product(self):
        contract_fiber_wrong_product_args = self.contract_fiber_args.copy()
        contract_fiber_wrong_product_args['service_supplier_id'] = self.ref(
            'somconnexio.service_supplier_vodafone'
        )
        contract_fiber_wrong_product_args['contract_line_ids'] = [(0, False, {
            "name": "ADSL 20Mb",
            "product_id": self.product_broadband_adsl.id
        })]
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_fiber_wrong_product_args]
        )
