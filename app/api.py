from woocommerce import API

from settings import *

from misc import safe_cast, logger

from product import Product

from field import VariantAttributeField

from functools import lru_cache

wcapi = API(
    url=WEBSITE_URL,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    version=API_VERSION,
    timeout=TIMEOUT
)


def get_product(product_id=None, **kwargs):
    if product_id is None:
        safe_product_id = ""
    else:
        safe_product_id = safe_cast(product_id, int, 0)
        if not safe_product_id:
            raise AttributeError("product_id should be integer larger than 0")
    logger.debug(f"Getting products from endpoint: products/{safe_product_id}")
    return wcapi.get(f'products/{safe_product_id}',
                     params={'per_page': 9999, 'status': 'publish', **kwargs}).json()


def get_product_variants(product_id=None, **kwargs):
    safe_product_id = safe_cast(product_id, int, 0)
    if not safe_product_id:
        raise AttributeError("product_id should be integer larger than 0")

    logger.debug(f"Getting variants from endpoint: products/{product_id}/variations")
    return wcapi.get(f'products/{product_id}/variations',
                     params={'per_page': 99, 'status': 'publish', **kwargs}).json()


@lru_cache
def get_category(category_id=None, **kwargs):
    if category_id is None:
        safe_category_id = ""
    else:
        safe_category_id = safe_cast(category_id, int, 0)

    if not safe_category_id:
        logger.warn(f"'{category_id}' is not proper category_id. That is not going to be queried.")
        return ""

    logger.debug(f"Getting categories from endpoint: products/categories/{safe_category_id}")
    return wcapi.get(f'products/categories/{safe_category_id}',
                     params={'per_page': 99, 'status': 'publish', **kwargs}).json()


def get_variants_as_products(product_id=None, fieldset=[], product_get_params={}, variant_get_params={}):
    product_set = []
    logger.info(f'Downloading product{"s" if product_id is None else f" {product_id}"}')
    products = get_product(product_id, **product_get_params)
    for pd in products:
        prod_id = pd['id']
        if 'type' in pd and pd['type'] == 'variable':
            logger.info(f"Downloading variants of product {prod_id}")
            variants = get_product_variants(prod_id, **variant_get_params)
            for pvd in variants:
                product = Product()
                product.fields = fieldset
                for field in product.fields:
                    if not isinstance(field, VariantAttributeField):
                        if field.is_variant_field():
                            field.value_from_dict(pvd)
                        else:
                            field.value_from_dict(pd)
                    else:
                        field.value_from_dict(pvd, pd)
                product_set.append(product)
        else:
            product = Product()
            product.fields = fieldset
            for field in product.fields:
                field.value_from_dict(pd)
            product_set.append(product)
    return product_set

