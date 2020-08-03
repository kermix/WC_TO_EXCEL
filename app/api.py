from woocommerce import API

from settings import *

from misc import safe_cast, logger

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


def get_category(category_id=None, **kwargs):
    if category_id is None:
        safe_category_id = ""
    else:
        safe_category_id = safe_cast(category_id, int, 0)
        if not safe_category_id:
            raise AttributeError("product_id should be integer larger than 0")

    logger.debug(f"Getting variants from endpoint: products/categories/{safe_category_id}")
    return wcapi.get(f'products/categories/{safe_category_id}',
                     params={'per_page': 99, 'status': 'publish', **kwargs}).json()


def get_variants_as_products(product_id=None, fieldset=[], product_get_params={}, variant_get_params={}):
    products = get_product(product_id, **product_get_params)
    for pd in products:
        logger.info(f'Downloading product {prod_id}')
        prod_id = pd['id']
        if 'type' in pd and pd['type'] == 'variable':
            variants = get_product_variants(prod_id, **variant_get_params)
            for pvd in variants:
                logger.info(f"Downloading variant {variant_id} of product {prod_id}")
                variant_id = pvd['id']
                continue
