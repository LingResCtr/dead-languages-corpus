from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from corpus import Corpus, Element, Gloss, HeadWord, Language


@dataclass
class Token:
    text: str
    parts_of_speech: list[str]
    parts_of_speech_ext: list[str]
    en_text: str
    en_keywords: list[str]


@dataclass
class Sentence:
    id: int
    language: str
    text: str
    en_text: str
    tokens: list[Token]


def parse_sentences(corpus: Corpus) -> list[Sentence]:
    """Turns the corpus into a list of sentences read to be dumped to JSONlines files"""
    sentences: list[Sentence] = []

    print("Mapping glossed texts to languages")
    glossed_text_to_language = get_glossed_text_to_language_map(corpus)

    print("Mapping glossed texts to translations")
    glossed_text_to_translation = get_glossed_text_to_translation_map(corpus)

    print("Mapping glosses to elements")
    gloss_to_elements = get_gloss_to_elements_map(corpus)

    print("Mapping glossed texts to glosses")
    glossed_text_to_glosses = get_glossed_text_to_glosses_map(corpus)

    print("Mapping glossed text to tokens")
    glossed_text_to_tokens = get_glossed_text_to_tokens_map(
        corpus=corpus,
        gloss_to_elements=gloss_to_elements,
        glossed_text_to_glosses=glossed_text_to_glosses,
    )

    for id, row in corpus.glossed_text.items():
        language = glossed_text_to_language[id]
        text = row.glossed_text
        en_text = glossed_text_to_translation[id]
        tokens = glossed_text_to_tokens[id]

        sentences.append(Sentence(
            id=id,
            language=language,
            text=text,
            en_text=en_text,
            tokens=tokens
        ))

    return sentences


def get_glossed_text_to_language_map(corpus: Corpus) -> dict[int, str]:
    """Creates a map of glossed text ids to language abbreviations"""
    id_to_lang = {}
    for id, row in corpus.glossed_text.items():
        lesson = corpus.lesson[row.lesson_id]
        langauge = corpus.language[lesson.language_id]
        id_to_lang[id] = langauge.lang_attribute
    return id_to_lang


def get_glossed_text_to_translation_map(corpus: Corpus) -> dict[int, str]:
    """Creates a map of glossed text ids to English translations"""
    id_to_en = {}
    for id, row in corpus.glossed_text.items():
        id_to_en[id] = "FOO"  # TODO: actually look this up
    return id_to_en


def get_gloss_to_elements_map(corpus: Corpus) -> dict[int, list[Element]]:
    """Creates a map of glossed text ids to lists of tokens in the text"""
    id_to_elements = defaultdict(list)
    for id, row in corpus.element.items():
        id_to_elements[row.gloss_id].append(row)

    for id in id_to_elements.keys():
        id_to_elements[id].sort(key=lambda e: e.order)

    return id_to_elements


def get_glossed_text_to_glosses_map(corpus: Corpus) -> dict[int, list[Gloss]]:
    """Creates a map of glossed text ids to lists of tokens in the text"""
    id_to_glosses = defaultdict(list)
    for id, row in corpus.gloss.items():
        id_to_glosses[row.glossed_text_id].append(row)

    for id in id_to_glosses.keys():
        try:
            id_to_glosses[id].sort(key=lambda e: e.order)
        except:
            print(id_to_glosses[id])
            raise

    return id_to_glosses


def get_glossed_text_to_tokens_map(
    corpus: Corpus,
    gloss_to_elements: dict[int, Element],
    glossed_text_to_glosses: dict[int, Gloss],
) -> dict[int, list[Token]]:
    """Creates a map of glossed text ids to lists of tokens in the text"""
    id_to_tokens = {}
    for id, row in corpus.glossed_text.items():
        glosses = glossed_text_to_glosses[id]
        tokens = []
        for gloss in glosses:
            parts_of_speech = [
                element.part_of_speech for element in gloss_to_elements[gloss.id]
            ]
            parts_of_speech_ext = [
                element.part_of_speech_ext for element in gloss_to_elements[gloss.id]
            ]
            keywords = [
                corpus.head_word[element.head_word_id].keywords.split(",")
                for element in gloss_to_elements[gloss.id]
            ]
            token = Token(
                text=gloss.surface_form,
                parts_of_speech=parts_of_speech,
                parts_of_speech_ext=parts_of_speech_ext,
                en_text=gloss.contextual_gloss,
                en_keywords=keywords
            )
            tokens.append(token)

    return id_to_tokens
