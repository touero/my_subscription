import os
from enum import Enum, unique


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOT_FILE = os.path.join(BASE_DIR, "hot.html")
TEMPLATE = os.path.join(BASE_DIR, "template")
TEMPLATE_HTML = os.path.join(TEMPLATE, "template.html")


@unique
class Url(Enum):
    WeiBo = "https://tophub.today/n/KqndgxeLl9"
    Zhihu = "https://tophub.today/n/mproPpoq6O"
