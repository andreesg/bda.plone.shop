from decimal import Decimal
from bda.plone.checkout.interfaces import ICheckoutSettings
from bda.plone.orders.interfaces import STATE_RESERVED
from bda.plone.orders.interfaces import STATE_MIXED
from bda.plone.orders.common import OrderData
from bda.plone.shop.utils import get_shop_payment_settings
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ICheckoutSettings)
@adapter(Interface)
class CheckoutSettings(object):

    def __init__(self, context):
        self.context = context

    def skip_payment(self, uid):
        settings = get_shop_payment_settings()
        order_data = OrderData(self.context, uid=uid)
        # order total is 0, skip
        if not Decimal(str(order_data.total)).quantize(Decimal('1.000')):
            return True
        # if payment should be skipped if order contains reservations and
        # order contains reservations, skip
        if settings.skip_payment_if_order_contains_reservations:
            if order_data.state in (STATE_RESERVED, STATE_MIXED):
                return True
        return False

    def skip_payment_redirect_url(self, uid):
        base = '%s/@@mollie_payment_success?order_uid=%s'
        return base % (self.context.absolute_url(), uid)
