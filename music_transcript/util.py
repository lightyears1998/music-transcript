import langdetect


def detect_language(text: str):
    possible_langs = ["zh-cn", "ja", "en", "de", "fr"]
    detected_possible_langs = langdetect.detect_langs(text)
    for lang in detected_possible_langs:
        lang = str(lang).split(':')[0]
        if lang in possible_langs:
            return lang
    return "zh-cn"


if __name__ == "__main__":
    pass
