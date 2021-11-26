import requests
import os
import yaml
try:
    from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
    from yaml import YamlLoader, YamlDumper

API = os.getenv("NETEASE_API") or "http://localhost:3000"
RAW_COOKIE = os.getenv("NETEASE_COOKIE") or \
    r"JSESSIONID-WYYY=aaaa; KEY2=bbbb; KEY3=cccc" # 请求 https://music.163.com/xxxapi/ 时用的 Cookie
DATA_DIR = os.path.normpath(os.getenv("MUSIC_TRANSCRIPT_DATA_DIR") or "{}/data".format(os.getcwd()))

def pre_process_cookie():
    # Binaryify / NeteaseCloudMusicApi 会把 "A=aaaa; B=bbbb" 形式的 Cookie 处理为 { "A": "aaaa", " B": "bbbb" }，
    # 第二个键 " B" 不符合 Cookie 规范，故需要对 Cookie 进行预处理，去掉 Cookie 各项之间的空格。
    return ''.join(RAW_COOKIE.split(' '))

cookie = pre_process_cookie()

def get_path(path):
    return os.path.normpath("{}/{}".format(DATA_DIR, path))

def bootstrap():
    print("Using DATA_DIR", DATA_DIR)

    dirs = ["songs", "playlists"]
    dirs = list(map(lambda dir: get_path(dir), dirs))
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)

def cache(path, data=None):
    if not data:
        try:
            with open(path, "r", encoding='utf8') as f:
                return yaml.load(f.read(), Loader=YamlLoader)
        except FileNotFoundError:
            return
    else:
        with open(path, "w", encoding='utf8') as f:
            f.write(yaml.dump(data, Dumper=YamlDumper, allow_unicode=True))
        return data

def cache_song_list(list_id, data=None):
    path = get_path("playlists/{}.yaml".format(str(list_id)))
    return cache(path, data)

def get_song_list(list_id: int) -> list[int]:
    cache = cache_song_list(list_id)
    if cache:
        return cache
    else:
        out = requests.post(API + "/playlist/detail", {
            "id": str(list_id),
            "cookie": cookie
        })

        song_list = out.json()
        return cache_song_list(list_id, song_list)


def get_lyrics(song_id: int) -> None:
    out = requests.post(API + "/lyric", {
        "id": str(song_id)
    }).json()
    lrc = out['lrc']
    if lrc and lrc['lyric']:
        print(lrc['lyric'])

if __name__ == "__main__":
    bootstrap()
    get_song_list(162317931)
    # get_lyrics(572468962)
