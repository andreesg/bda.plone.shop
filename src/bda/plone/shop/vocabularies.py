# -*- coding: utf-8 -*-
from bda.plone.checkout.vocabularies import country_vocabulary
from bda.plone.checkout.vocabularies import gender_vocabulary
from bda.plone.payment import Payments
from bda.plone.shipping import Shippings
from bda.plone.shop import message_factory as _
from bda.plone.shop.utils import get_shop_article_settings
from bda.plone.shop.utils import get_shop_tax_settings
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


# This are the overall avaiable quantity units which then can be reduced in
# control panel. If you need to provide more quantity units add it here or
# patch this vocab
AVAILABLE_QUANTITY_UNITS = {
    'quantity': _('quantity', default='Quantity'),
    'meter': _('meter', default='Meter'),
    'kilo': _('kilo', default='Kilo'),
    'liter': _('liter', default='Liter'),
}


@provider(IVocabularyFactory)
def AvailableQuantityUnitVocabulary(context):
    # vocab is used in shop settings control panel
    items = AVAILABLE_QUANTITY_UNITS.items()
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


@provider(IVocabularyFactory)
def QuantityUnitVocabulary(context):
    # vocab is used for buyable items
    try:
        settings = get_shop_article_settings()
    except KeyError:
        # happens GS profile application if registry entries not present yet
        return AvailableQuantityUnitVocabulary(context)
    if not settings:
        return
    terms = []
    for quantity_unit in settings.quantity_units:
        title = AVAILABLE_QUANTITY_UNITS.get(quantity_unit, quantity_unit)
        terms.append(SimpleTerm(value=quantity_unit, title=title))
    return SimpleVocabulary(terms)


# This are the overall avaiable VAT values which then can be reduced in
# control panel. If you need to provide more vat values add it here or
# patch this vocab
AVAILABLE_VAT_VALUES = {
    '0': '0%',
    '2.5': '2,5%',
    '3.8': '3,8%',
    '6': '6%',
    '8': '8%',
    '10': '10%',
    '15': '15%',
    '20': '20%',
    '21': '21%',
    '25': '25%',
}


@provider(IVocabularyFactory)
def AvailableVatVocabulary(context):
    # vocab is used in shop settings control panel
    items = AVAILABLE_VAT_VALUES.items()
    items = sorted(items, key=lambda x: x[0])
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


@provider(IVocabularyFactory)
def VatVocabulary(context):
    # vocab is used for buyable items.
    try:
        settings = get_shop_tax_settings()
    except KeyError:
        # happens GS profile application if registry entries not present yet
        return AvailableVatVocabulary(context)
    settings.vat
    terms = []
    if settings.vat:
        for vat in settings.vat:
            title = AVAILABLE_VAT_VALUES.get(vat, vat)
            terms.append(SimpleTerm(value=vat, title=title))
    return SimpleVocabulary(terms)


# This are the overall avaiable currency values available in
# control panel. If you need to provide more currencies add it here or
# patch this vocab
AVAILABLE_CURRENCIES = {
    'EUR': _('EUR', default='Euro'),
    'USD': _('USD', default='US Dollar'),
    'INR': _('INR', default='Indian Rupee'),
    'CAD': _('CAD', default='Canadian Dollar'),
    'CHF': _('CHF', default='Swiss Franc'),
    'GBP': _('GBP', default='British Pound Sterling'),
    'AUD': _('AUD', default='Australian Dollar'),
    'NOK': _('NOK', default='Norwegian Krone'),
    'SEK': _('SEK', default='Swedish Krona'),
    'DKK': _('DKK', default='Danish Krone'),
    'YEN': _('YEN', default='Japanese Yen'),
    'NZD': _('NZD', default='New Zealand Dollar'),
}


@provider(IVocabularyFactory)
def AvailableCurrenciesVocabulary(context):
    items = AVAILABLE_CURRENCIES.items()
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


@provider(IVocabularyFactory)
def CurrencyDisplayOptionsVocabulary(context):
    items = [
        ('yes', _('yes', default='Yes')),
        ('no', _('no', default='No')),
        ('symbol', _('symbol', default='Symbol')),
    ]
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


@provider(IVocabularyFactory)
def GenderVocabulary(context):
    return SimpleVocabulary([SimpleTerm(value=k, title=v)
                             for k, v in gender_vocabulary()])


@provider(IVocabularyFactory)
def CountryVocabulary(context):
    """VocabularyFactory for countries from ISO3166 source.
    """
    return SimpleVocabulary([SimpleTerm(value=k, title=v)
                             for k, v in country_vocabulary()])


@provider(IVocabularyFactory)
def AvailableShippingMethodsVocabulary(context):
    shippings = Shippings(context).shippings
    items = [(shipping.sid, shipping.label) for shipping in shippings]
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


@provider(IVocabularyFactory)
def ShippingMethodsVocabulary(context):
    try:
        items = Shippings(context).vocab
    except KeyError:
        # happens GS profile application if registry entries not present yet
        return AvailableShippingMethodsVocabulary(context)
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


@provider(IVocabularyFactory)
def AvailablePaymentMethodsVocabulary(context):
    payments = Payments(context).payments
    items = [(payment.pid, payment.label) for payment in payments]
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


@provider(IVocabularyFactory)
def PaymentMethodsVocabulary(context):
    try:
        items = Payments(context).vocab
    except KeyError:
        # happens GS profile application if registry entries not present yet
        return AvailablePaymentMethodsVocabulary(context)
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])
