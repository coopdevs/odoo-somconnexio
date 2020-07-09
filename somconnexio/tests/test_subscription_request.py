from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class TestSubscription(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.SubscriptionRequest = self.env['subscription.request']
        self.vals_subscription = {
            'already_cooperator': False,
            'name': 'Manuel Dublues Test',
            'email': 'manuel@demo-test.net',
            'ordered_parts': 1,
            'address': 'schaerbeekstraat',
            'city': 'Brussels',
            'zip_code': '1111',
            'country_id': 20,
            'date': datetime.now() - timedelta(days=12),
            'company_id': 1,
            'source': 'manual',
            'share_product_id': False,
            'lang': 'en_US',
            'sponsor_id': False,
            'iban': 'ES6020808687312159493841'
        }
        CoopAgreement = self.env['coop.agreement']
        vals_coop_agreement = {
            'partner_id': self.ref("easy_my_coop.res_partner_cooperator_1_demo"),
            'products': False,
            'code': 'CODE',
        }
        self.coop_agreement = CoopAgreement.create(vals_coop_agreement)
        return result

    def test_create_subscription_coop_agreement_sponsorship(self):
        vals_subscription_sponsorship = self.vals_subscription.copy()
        vals_subscription_sponsorship.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': self.coop_agreement.id,
        })
        subscription = self.SubscriptionRequest.create(vals_subscription_sponsorship)
        self.assertEqual(subscription.subscription_amount, 0.0)

    def test_create_subscription_coop_agreement_sponsorship_without_coop_agreement_raise_validation_error(self):  # noqa
        vals_subscription_sponsorship = self.vals_subscription.copy()
        vals_subscription_sponsorship.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': False,
        })

        self.assertRaises(
            ValidationError,
            self.SubscriptionRequest.create,
            vals_subscription_sponsorship
        )

    def test_validate_subscription_coop_agreement_sponsorship(self):
        vals_subscription_sponsorship = self.vals_subscription.copy()
        vals_subscription_sponsorship.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': self.coop_agreement.id,
        })
        subscription = self.SubscriptionRequest.create(vals_subscription_sponsorship)
        subscription.validate_subscription_request()

        partner = subscription.partner_id
        self.assertEqual(partner.coop_agreement_id.id, self.coop_agreement.id)

        self.assertFalse(partner.coop_candidate)
        self.assertFalse(partner.coop_sponsee)
        self.assertTrue(partner.coop_agreement)
