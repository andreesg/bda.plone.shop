# -*- coding: utf-8 -*-
from decimal import Decimal
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from bda.plone.shop.interfaces import IShopArticleSettings
from bda.plone.shop.interfaces import IShopCartSettings
from bda.plone.shop.interfaces import IShopSettings
from bda.plone.shop.interfaces import IShopShippingSettings
from bda.plone.shop.interfaces import IShopTaxSettings
from bda.plone.shop.interfaces import INotificationTextSettings
from bda.plone.shop.interfaces import IPaymentTextSettings

ALLOWED_TYPES_TICKETS = ['Event']

def format_amount(val):
    val = val.quantize(Decimal('1.00'))
    if bool(val % 2):
        return str(val).replace('.', ',')
    return str(val.quantize(Decimal('1'))) + ',-'


def get_shop_settings():
    return getUtility(IRegistry).forInterface(IShopSettings)


def get_shop_tax_settings():
    return getUtility(IRegistry).forInterface(IShopTaxSettings)


def get_shop_article_settings():
    return getUtility(IRegistry).forInterface(IShopArticleSettings)


def get_shop_cart_settings():
    return getUtility(IRegistry).forInterface(IShopCartSettings)


def get_shop_shipping_settings():
    return getUtility(IRegistry).forInterface(IShopShippingSettings)


def get_shop_notification_settings():
    return getUtility(IRegistry).forInterface(INotificationTextSettings)


def get_shop_payment_settings():
    return getUtility(IRegistry).forInterface(IPaymentTextSettings)

def is_ticket(context):
    if context:
        if "/tickets" in context.absolute_url():
            return True

        if context.portal_type in ALLOWED_TYPES_TICKETS:
            physical_path = context.getPhysicalPath()
            path = "/".join(physical_path)

            results = context.portal_catalog(path={'query': path, 'depth': 1}, portal_type="product", Subject="ticket")
            if len(results) > 0:
                return True

        return False
    else:
        return False