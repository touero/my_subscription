import os
from enum import Enum, unique


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOT_FILE = os.path.join(BASE_DIR, "hot.html")
TEMPLATE = os.path.join(BASE_DIR, "template")
TEMPLATE_HTML = os.path.join(TEMPLATE, "template.html")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",

    "Referer": "https://tophub.today/"
}


@unique
class Url(Enum):
    WeiBo = "https://tophub.today/n/KqndgxeLl9"
    Zhihu = "https://tophub.today/n/mproPpoq6O"

    @staticmethod
    def url_favicon_icon(url):
        if 'weibo' in url:
            return "https://weibo.com/favicon.ico"
        elif 'zhihu' in url:
            return "https://static.zhihu.com/heifetz/favicon.ico"
        else:
            return ''
