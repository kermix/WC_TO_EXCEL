from woocommerce import API

from settings import *

wcapi = API(
    url=WEBSITE_URL,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    version=API_VERSION,
    timeout=TIMEOUT
)