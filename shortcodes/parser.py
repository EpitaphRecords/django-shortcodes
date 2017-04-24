import re
import shortcodes.parsers
from django.core.cache import cache


def import_parser(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def create_cache_key(shortcode):
    """
    Take a shortcode and create a cache key that the cache backends should be happy with
    """
    cache_key = re.sub(r'\s+', '_', shortcode)

    # Remove characters that memcache doesn't like
    # This is referenced from the validate_key function in the BaseCache
    # class in Django

    remove = []

    for char in cache_key:
        if ord(char) < 33 or ord(char) == 127:
            remove.append(char)

    for char in set(remove):
        cache_key = cache_key.replace(char, '')

    return cache_key


def parse(value):
    ex = re.compile(r'\[(.*?)\]')
    groups = ex.findall(value)
    pieces = {}
    parsed = value

    for item in groups:
        if ' ' in item:
            name, space, args = item.partition(' ')
            args = __parse_args__(args)
        # If shortcode does not use spaces as a separator, it might use equals
        # signs.
        elif '=' in item:
            name, space, args = item.partition('=')
            args = __parse_args__(args)
        else:
            name = item
            args = {}

        cache_key = create_cache_key(item)

        try:
            if cache.get(cache_key):
                parsed = re.sub(r'\[' + re.escape(item) + r'\]', cache.get(cache_key), parsed)
            else:
                module = import_parser('shortcodes.parsers.' + name)
                function = getattr(module, 'parse')
                result = function(args)
                cache.set(cache_key, result, 3600)
                parsed = re.sub(r'\[' + item + r'\]', result, parsed)
        except ImportError:
            pass

    return parsed


def __parse_args__(value):
    ex = re.compile(r'[ ]*(\w+)=([^" ]+|"[^"]*")[ ]*(?: |$)')
    groups = ex.findall(value)
    kwargs = {}

    for group in groups:
        if group.__len__() == 2:
            item_key = group[0]
            item_value = group[1]

            if item_value.startswith('"'):
                if item_value.endswith('"'):
                    item_value = item_value[1:]
                    item_value = item_value[:item_value.__len__() - 1]

            kwargs[item_key] = item_value

    return kwargs
