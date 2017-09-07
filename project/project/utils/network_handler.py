import random
from typing import Dict


class NetworkUtils:

    def get_user_agent() -> Dict:
        USER_AGENTS_LIST = [
            'Mozilla/4.0(compatible;'
            ' MSIE 7.0;Windows NT 5.1)',
            'Mozilla/5.0(Windows NT 6.1;'
            ' WOW64;rv:40.0)Gecko/20100101 Firefox/40.1',
            'Mozilla/5.0(X11;'
            ' OpenBSD amd64;rv:28.0) Gecko/20100101 Firefox/28.0',
            'Mozilla/5.0(Windows NT 6.1)'
            ' AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0(Windows NT 6.3;'
            ' Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/37.0.2049.0 Safari/537.36',
            'Mozilla/5.0(Windows NT 6.1;'
            ' WOW64) AppleWebKit/537.36(KHTML, like Gecko)'
            ' Chrome/36.0.1985.67 Safari/537.36',
            'Mozilla/5.0(Macintosh; Intel Mac OS X 10_10_4)'
            ' AppleWebKit/600.7.12(KHTML, like Gecko)'
            ' Version/8.0.7 Safari/600.7.12'
        ]
        return {'USERAGENT': random.choice(USER_AGENTS_LIST)}
