import re
import random
import string

URL_REGEX = re.compile(
    r'^(https?://)'  # http:// or https://
    r'([\w.-]+)'    # domain
    r'(:\d+)?'      # optional port
    r'(/[\w./?%&=-]*)?$', re.IGNORECASE
)

def is_valid_url(url):
    return bool(URL_REGEX.match(url))

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))