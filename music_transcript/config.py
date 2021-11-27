import os
import logging
import jieba


API = os.getenv("NETEASE_API") or "http://localhost:3000"


DATA_DIR = os.path.normpath(os.getenv("MUSIC_TRANSCRIPT_DATA_DIR") or "{}/data".format(os.getcwd()))

RAW_COOKIE = os.getenv("NETEASE_COOKIE") or \
    r"JSESSIONID-WYYY=aaaa; KEY2=bbbb; KEY3=cccc" # 请求 https://music.163.com/xxxapi/ 时用的 Cookie


def pre_process_cookie():
    # Binaryify / NeteaseCloudMusicApi 会把 "A=aaaa; B=bbbb" 形式的 Cookie 处理为 { "A": "aaaa", " B": "bbbb" }，
    # 第二个键 " B" 不符合 Cookie 规范，故需要对 Cookie 进行预处理，去掉 Cookie 各项之间的空格。
    return ''.join(RAW_COOKIE.split(' '))


COOKIE = pre_process_cookie()

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
