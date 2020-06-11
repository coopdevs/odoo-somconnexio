from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta


class TestSubscription(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.SubscriptionRequest = self.env['subscription.request']
        self.product_template_test = self.env['product.template'].create({
            'name': 'Part T - Test',
            'short_name': 'Part T',
            'is_share': True,
            'default_share_product': True,
            'force_min_qty': True,
            'minimum_quantity': 1,
            'by_individual': True,
            'by_company': True,
            'list_price': 100,
            'display_on_website': True
        })
        self.vals_subscription_regular = {
            'already_cooperator': False,
            'name': 'Manuel Dublues Test',
            'email': 'manuel@demo-test.net',
            'ordered_parts': 1,
            'address': 'schaerbeekstraat',
            'city': 'Brussels',
            'zip_code': '1111',
            'country_id': 20,
            'date': datetime.now()-timedelta(days=12),
            'company_id': 1,
            'source': 'manual',
            'share_product_id': self.product_template_test.product_variant_id.id,
            'lang': 'en_US'
            }
        return result

    def test_create_subscription_regular(self):
        subscription_regular = self.SubscriptionRequest.create(self.vals_subscription_regular)
        self.assertEqual(subscription_regular.subscription_amount, 100.0)

    def test_create_subscription_refered(self):
        vals_subscription_refered = self.vals_subscription_regular.copy()
        vals_subscription_refered.update({'share_product_id': False, 'ordered_parts': False})
        subscription_regular = self.SubscriptionRequest.create(vals_subscription_refered)
        self.assertEqual(subscription_regular.subscription_amount, 0.0)
