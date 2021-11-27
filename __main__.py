from music_transcript.crawler import *
from music_transcript.analyzer import *


def main():
    bootstrap()
    # list = get_playlist(162317931)
    # expand_list_and_get_lyrics(list)
    # extract_lyrics_text_for_all()
    text = cut_all_text()
    wordclouds = generate_wordclouds(text)
    # wordclouds['zh-cn'].to_file(get_path("wordcloud.png"))
    # svg = wordclouds['zh-cn'].to_svg()
    # with open(get_path("wordcloud.svg"), "w", encoding="utf8") as f:
    #     f.write(svg)
    show_wordcloud(wordclouds['zh-cn'])
    show_wordcloud(wordclouds['en'])
    show_wordcloud(wordclouds['ja'])


if __name__ == "__main__":
    main()
