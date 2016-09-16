from bda.plone.shop.tests import set_browserlayer
from bda.plone.shop.tests import ShopAT_INTEGRATION_TESTING

import unittest2 as unittest


class TestATIntegration(unittest.TestCase):
    layer = ShopAT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        set_browserlayer(self.request)

    def test_foo(self):
        self.assertEquals(1, 1)
