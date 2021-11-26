from typing import Tuple
import requests
import yaml
try:
    from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
    from yaml import YamlLoader, YamlDumper
import time
import random
from .config import *


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
            "cookie": COOKIE
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
