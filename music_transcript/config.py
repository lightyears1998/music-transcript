import os
import logging
import jieba


API = os.getenv("NETEASE_API") or "http://localhost:3000"


DATA_DIR = os.path.normpath(os.getenv("MUSIC_TRANSCRIPT_DATA_DIR") or "{}/data".format(os.getcwd()))

RAW_COOKIE = os.getenv("NETEASE_COOKIE") or \
    r"JSESSIONID-WYYY=aaaa; KEY2=bbbb; KEY3=cccc" # cookies used in https://music.163.com/xxxapi/


def __pre_process_cookie():
    # `Binaryify / NeteaseCloudMusicApi` handles cookies of the form `A=aaaa; B=bbbb` as `{ "A": "aaaa", " B": "bbbb" }`.
    # The second key `" B"` which contains a space in its name does not conform to the cookie specification and result in bugs,
    # so the cookie needs to be pre-processed to remove the spaces between the cookie items.
    return ''.join(RAW_COOKIE.split(' '))


COOKIE = __pre_process_cookie()

UNICODE_FONT = "C:\Windows\Fonts\SourceHanSans.ttc"

VALID_LANGUAGES = ["zh-cn", "en", "ja"]


STOPWORDS = {
    "zh-cn": """
    我
    你
    他
    她
    的
    谁
    了
    那
    有
    没有
    却
    是
    不是
    是不是
    与
    和
    啦
    在
    也
    都
    着
    又
    还
    要
    去
    就
    把
    来
    到
    最
    啊
    什么
    不
    这""",
    "en": """
    you
    I
    he""",
    "ja": """
    """
}
for lang in STOPWORDS.keys():
    words = STOPWORDS[lang].split('\n')
    words = map(lambda word: word.strip(), words)
    STOPWORDS[lang] = set(words)


def get_path(path):
    return os.path.normpath("{}/{}".format(DATA_DIR, path))


def __init_jieba():
    jieba.setLogLevel(logging.INFO)
    jieba.initialize()


def __create_data_direactory():
    print("Using DATA_DIR", DATA_DIR)

    dirs = ["lyrics", "playlists", "derivation/lyrics"]
    dirs = list(map(lambda dir: get_path(dir), dirs))
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def bootstrap():
    __init_jieba()
    __create_data_direactory()
