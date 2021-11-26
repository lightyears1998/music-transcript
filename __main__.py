from music_transcript.crawler import *
from music_transcript.analyzer import *


def main():
    bootstrap()
    list = get_playlist(162317931)
    expand_list_and_get_lyrics(list)


if __name__ == "__main__":
    main()
