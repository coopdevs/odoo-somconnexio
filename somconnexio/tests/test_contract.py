from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestContract(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Contract = self.env['contract.contract']
        self.product_1 = self.env.ref('product.product_product_1')

    def test_create_mobile_contract_with_mobile_service(self):
        self.product_1.categ_id = self.ref("somconnexio.mobile_service")

        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': self.ref("easy_my_coop.res_partner_cooperator_1_demo"),
            'contract_category_id': self.ref("somconnexio.mobile"),
            'contract_line_ids': [
                (
                    0,
                    0,
                    {
                        'product_id': self.product_1.id,
                        'name': 'Services from #START# to #END#',
                        'quantity': 1,
                        'recurring_rule_type': 'monthly',
                        'recurring_interval': 1,
                        'date_start': '2018-02-15',
                        'recurring_next_date': '2018-02-22',
                    },
                )
            ],
        }

        contract = self.Contract.create(vals_contract)

        self.assertEqual(contract.contract_category_id.name, 'Mobile')

    def test_create_mobile_contract_with_broadband_service_raise_ValidationError(self):
        self.product_1.categ_id = self.ref("somconnexio.broadband_service")

        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': self.ref("easy_my_coop.res_partner_cooperator_1_demo"),
            'contract_category_id': self.ref("somconnexio.mobile"),
            'contract_line_ids': [
                (
                    0,
                    0,
                    {
                        'product_id': self.product_1.id,
                        'name': 'Services from #START# to #END#',
                        'quantity': 1,
                        'recurring_rule_type': 'monthly',
                        'recurring_interval': 1,
                        'date_start': '2018-02-15',
                        'recurring_next_date': '2018-02-22',
                    },
                )
            ],
        }

        self.assertRaises(ValidationError, self.Contract.create, vals_contract)
