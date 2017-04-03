# -*- coding: utf-8 -*-
from bda.plone.shop.interfaces import INotificationTextSettings
from bda.plone.shop.interfaces import IPaymentTextSettings
from bda.plone.shop.interfaces import IShopArticleSettings
from bda.plone.shop.interfaces import IShopCartSettings
from bda.plone.shop.interfaces import IShopSettings
from bda.plone.shop.interfaces import IShopShippingSettings
from bda.plone.shop.interfaces import IShopTaxSettings
from decimal import Decimal
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

ALLOWED_TYPES_TICKETS = ['Event']
from decimal import Decimal

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


def find_context(request):
    published = request.get('PUBLISHED', None)
    context = getattr(published, '__parent__', None)
    if context is None:
        context = request.PARENTS[0]
    return context

def find_tickets(context):
    catalog = context.portal_catalog
    physical_path = context.getPhysicalPath()
    path = "/".join(physical_path)
    brains = catalog(path={'query': path, 'depth': 1}, portal_type='product', sort_on='getObjPositionInParent', Subject="ticket")
    return brains

def add_tickets(ret, context):
    tickets = find_tickets(context)

    # Populate ticket ids
    uids = []
    for ticket in tickets:
        uids.append((ticket.UID, Decimal(0), ''))
    
    for uid, count, comment in ret:
        for index, elem in enumerate(uids):
            if elem[0] == uid:
                uids[index] = (uid, Decimal(count), comment)
                break

    return uids

def remove_tickets(ret, context):
    tickets = find_tickets(context)

    uuids = []
    for ticket in tickets:
        uuids.append(ticket.UID)

    new_ret = []

    for item in ret:
        if item[0] not in uuids:
            new_ret.append(item)

    return new_ret

def extractTickets(ret, request):
    if request != None:
        context = find_context(request)

        if is_ticket(context):
            ret = add_tickets(ret, context)
        else:
            ret = remove_tickets(ret, context)

    return ret

