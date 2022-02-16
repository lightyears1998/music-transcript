from typing import List, Tuple
import requests
from functools import wraps
import yaml
try:
    from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
    from yaml import YamlLoader, YamlDumper
import time
import random
from .config import *


def read_cache(path):
    try:
        with open(path, "r", encoding='utf8') as f:
            return yaml.load(f.read(), Loader=YamlLoader)
    except FileNotFoundError:
        return


def write_cache(path, data):
    with open(path, "w", encoding='utf8') as f:
        f.write(yaml.dump(data, Dumper=YamlDumper, allow_unicode=True))
    return data


def caching(cache_path_builder):
    def cache_path_wrapper(func):
        @wraps(func)
        def cache_wrapper(*arg, **kwargs):
            cache_path = cache_path_builder(*arg)
            force_update = kwargs.pop('force_update', False)
            no_cache = kwargs.pop('no_cache', False)

            cached_result = read_cache(cache_path) if not force_update else None

            if cached_result:
                return cached_result, True
            else:
                result = func(*arg, **kwargs)
                if not no_cache:
                    write_cache(cache_path, result)
                return result, False

        return cache_wrapper
    return cache_path_wrapper


@caching(lambda playlist_id: get_path("playlists/{}.yaml".format(playlist_id)))
def get_playlist(playlist_id: int) -> List[int]:
    res = requests.post(API + "/playlist/detail", {
        "id": str(playlist_id),
        "cookie": COOKIE
    })

    song_list = res.json()
    return song_list


@caching(lambda song_id: get_path("lyrics/{}.yaml".format(song_id)))
def get_lyrics(song_id: int) -> Tuple[dict, bool]:
    res = requests.get(API + "/lyric?id={}".format(song_id))
    lyrics = res.json()
    return lyrics


def expand_list_and_get_lyrics(list):
    track_ids = list["playlist"]["trackIds"]
    total = len(track_ids)
    for i in range(total):
        song_id = track_ids[i]["id"]
        print("processing {} of {}, song_id={}".format(i+1, total, song_id))
        _, cache_hit = get_lyrics(song_id)
        if not cache_hit:
            time.sleep(random.random() * 5)
