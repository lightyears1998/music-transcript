from typing import Tuple
import requests
import os
import yaml
try:
    from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
    from yaml import YamlLoader, YamlDumper
import time
import random

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

    dirs = ["lyrics", "playlists"]
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

def cache_playlist(playlist_id, playlist=None):
    path = get_path("playlists/{}.yaml".format(playlist_id))
    return cache(path, playlist)

def get_playlist(playlist_id: int) -> list[int]:
    cache = cache_playlist(playlist_id)
    if cache:
        return cache
    else:
        res = requests.post(API + "/playlist/detail", {
            "id": str(playlist_id),
            "cookie": cookie
        })

        song_list = res.json()
        return cache_playlist(playlist_id, song_list)

def cache_lyrics(song_id: int, lyrics=None):
    path = get_path("lyrics/{}.yaml".format(song_id))
    return cache(path, lyrics)

def get_lyrics(song_id: int) -> Tuple[dict, bool]:
    cache = cache_lyrics(song_id)
    if cache:
        return cache, True
    else:
        res = requests.get(API + "/lyric?id={}".format(song_id))
        lyrics = res.json()
        return cache_lyrics(song_id, lyrics), False

def expand_list_and_get_lyrics(list):
    track_ids = list["playlist"]["trackIds"]
    total = len(track_ids)
    for i in range(total):
        song_id = track_ids[i]["id"]
        print("processing {} of {}, song_id={}".format(i+1, total, song_id))
        _, cache_hit = get_lyrics(song_id)
        if not cache_hit:
            time.sleep(random.random() * 5)

def main():
    bootstrap()
    list = get_playlist(162317931)
    expand_list_and_get_lyrics(list)

if __name__ == "__main__":
    main()
