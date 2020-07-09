from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class ServiceTechnologyTest(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.contract_broadband_args = {
            'name': 'Contract w/category contract to broadband',
            'contract_category_id': self.ref('somconnexio.broadband'),
            'partner_id': self.ref('easy_my_coop.res_partner_cooperator_2_demo'),
        }
        self.contract_mobile_args = {
            'name': 'Contract w/category contract to mobile',
            'contract_category_id': self.ref('somconnexio.mobile'),
            'partner_id': self.ref('easy_my_coop.res_partner_cooperator_2_demo'),
        }

    def test_right_adsl(self):
        contract_right_service_tech_args = self.contract_broadband_args.copy()
        contract_right_service_tech_args.update({
            'service_technology_id': self.ref(
                'somconnexio.service_technology_adsl'
            )
        })
        self.assertTrue(
            self.env['contract.contract'].create(
                contract_right_service_tech_args
            )
        )

    def test_wrong_adsl(self):
        contract_right_service_tech_args = self.contract_mobile_args.copy()
        contract_right_service_tech_args.update({
            'service_technology_id': self.ref(
                'somconnexio.service_technology_adsl'
            )
        })
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_right_service_tech_args]
        )

    def test_right_mobile(self):
        contract_right_service_tech_args = self.contract_mobile_args.copy()
        contract_right_service_tech_args.update({
            'service_technology_id': self.ref(
                'somconnexio.service_technology_mobile'
            )
        })
        self.assertTrue(
            self.env['contract.contract'].create(
                contract_right_service_tech_args
            )
        )

    def test_wrong_mobile(self):
        contract_right_service_tech_args = self.contract_broadband_args.copy()
        contract_right_service_tech_args.update({
            'service_technology_id': self.ref(
                'somconnexio.service_technology_mobile'
            )
        })
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_right_service_tech_args]
        )

    def test_right_fiber(self):
        contract_right_service_tech_args = self.contract_broadband_args.copy()
        contract_right_service_tech_args.update({
            'service_technology_id': self.ref(
                'somconnexio.service_technology_fiber'
            )
        })
        self.assertTrue(
            self.env['contract.contract'].create(
                contract_right_service_tech_args
            )
        )

    def test_wrong_fiber(self):
        contract_right_service_tech_args = self.contract_mobile_args.copy()
        contract_right_service_tech_args.update({
            'service_technology_id': self.ref(
                'somconnexio.service_technology_fiber'
            )
        })
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            [contract_right_service_tech_args]
        )
