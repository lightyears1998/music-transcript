from music_transcript.crawler import *
from music_transcript.analyzer import *


def main():
    bootstrap()
    # list = get_playlist(162317931)
    # expand_list_and_get_lyrics(list)
    # extract_lyrics_text_for_all()
    text = cut_text_for_all()
    wc = generate_word_cloud(text)
    wc.to_file(get_path("wordcloud.png"))
    svg = wc.to_svg()
    with open(get_path("wordcloud.svg"), "w", encoding="utf8") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
