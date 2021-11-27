import os


API = os.getenv("NETEASE_API") or "http://localhost:3000"


DATA_DIR = os.path.normpath(os.getenv("MUSIC_TRANSCRIPT_DATA_DIR") or "{}/data".format(os.getcwd()))

RAW_COOKIE = os.getenv("NETEASE_COOKIE") or \
    r"JSESSIONID-WYYY=aaaa; KEY2=bbbb; KEY3=cccc" # 请求 https://music.163.com/xxxapi/ 时用的 Cookie


def pre_process_cookie():
    # Binaryify / NeteaseCloudMusicApi 会把 "A=aaaa; B=bbbb" 形式的 Cookie 处理为 { "A": "aaaa", " B": "bbbb" }，
    # 第二个键 " B" 不符合 Cookie 规范，故需要对 Cookie 进行预处理，去掉 Cookie 各项之间的空格。
    return ''.join(RAW_COOKIE.split(' '))


COOKIE = pre_process_cookie()


def get_path(path):
    return os.path.normpath("{}/{}".format(DATA_DIR, path))


def bootstrap():
    print("Using DATA_DIR", DATA_DIR)

    dirs = ["lyrics", "playlists", "derivation/lyrics"]
    dirs = list(map(lambda dir: get_path(dir), dirs))
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
