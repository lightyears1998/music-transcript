import yaml
try:
    from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
    from yaml import YamlLoader, YamlDumper
import langdetect
from .config import *


def load_yaml(path: str):
    with open(path, 'r', encoding="utf8") as f:
        return yaml.load(f.read(), Loader=YamlLoader)


def dump_yaml(data: any):
    return yaml.dump(data, Dumper=YamlDumper, allow_unicode=True)


def detect_language(text: str):
    possible_langs = VALID_LANGUAGES
    detected_possible_langs = langdetect.detect_langs(text)
    for lang in detected_possible_langs:
        lang = str(lang).split(':')[0]
        if lang in possible_langs:
            return lang
    return "zh-cn"
