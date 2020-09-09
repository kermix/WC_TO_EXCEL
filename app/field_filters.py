from bs4 import BeautifulSoup

import re

from api import get_category

from misc import logger


def remove_disallowed_tags(s):
    soup = BeautifulSoup(s, 'html.parser')

    for tag_to_remove in soup.find_all(['div', 'img', 'block', 'hr', 'table']):
        tag_to_remove.decompose()

    for tag_to_replace in soup.find_all(['ol']):
        tag_to_replace.name = 'ul'

    for tag_to_extract in soup.find_all(['p', 'a', 'span']):
        tag_to_extract.unwrap()

    return str(soup).strip()


def list_to_semicolon_separated_sting(s):
    s = re.sub(r'^(?:\s*-\s*)?(.*)[.\s]*', r'\1; ', s, flags=re.MULTILINE).replace('\r', '')
    return s[:-2] if s[-2:] == "; " else s


def category_id_to_category_name(id):
    d = get_category(id)

    if 'name' in d:
        return d['name']

    logger.warn(f"Cannot find name for category id '{id}'. Saving just category id.")
    return id


def format_pcr_instruments_column(s):
    s = re.sub(r'^(.*:)\s+', r'\1 ', s, flags=re.MULTILINE)
    s = re.sub(r'\n+', r'; ', s, flags=re.MULTILINE)
    s = re.sub(r'(;\s*)+', '; ', s)
    return s.replace('\r', '')
