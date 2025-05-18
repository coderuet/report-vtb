
from typing import TypedDict


class CommonConstants:
    BROWSER_INFO: str = 'Chrome-98.04758102'
    CLIENT_INFO: str = '127.0.0.1;MacOSProMax'
    NULL_HEADER = {  # type: ignore
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'vi-VN',
        "Accept": 'application/json',
        'Cache-Control': 'no-store, no-cache',
        'User-Agent': 'okhttp/3.11.0',
    }
