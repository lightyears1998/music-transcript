import os
import re
from typing import Dict
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from music_transcript.util import load_yaml
from .config import *
from .util import detect_language


def extract_lyrics_text(raw_lyrics: str):
    lines = raw_lyrics.split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        pattern = r"(?:\[\d{2}\:\d{2}(?:\.\d+)?\])+(.*)"
        match = re.search(pattern, lines[i])
        if match and len(match.groups()) >= 1:
            lines[i] = match.group(1).strip()
    return '\n'.join(lines)


def extract_all_lyrics_text():
    origin_lyrics_path = get_path("lyrics")
    filenames = os.listdir(origin_lyrics_path)
    for filename in filenames:
        input_file_path = get_path("lyrics/{}".format(filename))
        lyrics = load_yaml(input_file_path)
        raw_lyrics = lyrics["lrc"]["lyric"]
        extracted_lyrics = extract_lyrics_text(raw_lyrics)

        song_id, _ = os.path.splitext(filename)
        output_file_path = get_path("derivation/lyrics/{}.txt".format(song_id))
        with open(output_file_path, "w", encoding="utf8") as f:
            f.write(extracted_lyrics)


def cut_all_text() -> Dict[str, str]:
    dir = get_path("derivation/lyrics")

    text = {}
    for lang in VALID_LANGUAGES:
        text[lang] = ''

    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        with open(path, 'r', encoding="utf8") as f:
            content = f.read().strip()
            if len(content) == 0:
                continue

            content_lang = detect_language(content)
            if content_lang == 'zh-cn':
                content = ' '.join(jieba.cut(content))
                text['zh-cn'] = text['zh-cn'] + '\n' + content
            elif content_lang == 'ja':
                text['ja'] = text['ja'] + '\n' + content
            elif content_lang == 'en':
                text['en'] = text['en'] + '\n' + content
            else:
                pass
    return text


def generate_wordclouds(text):
    wordclouds = {}
    for lang in VALID_LANGUAGES:
        if len(text[lang]) == 0:
            continue
        wordclouds[lang] = WordCloud(width=1920, height=1080, scale=2, background_color="white", max_words=2000, font_path=UNICODE_FONT, stopwords=STOPWORDS[lang])
        wordclouds[lang].generate(text[lang])
    return wordclouds


def show_wordcloud(wordcloud):
    plt.figure(figsize=(16, 9))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
