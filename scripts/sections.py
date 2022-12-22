from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from clean import clean_html, clean_whitespace
from corpus import Corpus, Element, Gloss, GlossedText


@dataclass
class POS:
    part_of_speech: str
    analysis: Optional[str]


@dataclass
class Token:
    id: int             # maps to gloss id
    text: str
    parts_of_speech: list[POS]
    en_text: str
    en_keywords: list[list[str]]


@dataclass
class Chunk:
    id: int             # maps to glossed_text id
    text: str
    en_text: str
    tokens: list[Token]


@dataclass
class Section:
    id: int             # maps to lesson id
    lesson_url: str
    language: str
    chunks: list[Chunk]
    raw_html: str
    en_html: str


def parse_sections(corpus: Corpus) -> list[Section]:
    """Turns the corpus into a list of sections read to be dumped to JSONlines files"""
    sections: list[Section] = []

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

    n_chunks = 0
    n_sections = 0

    for lesson_id, lesson in corpus.lesson.items():
        # skip lessons that don't have language to contribute to this data set
        if lesson.lesson_translation is None:
            continue

        glossed_texts = sorted(
            [gt for gt in corpus.glossed_text.values() if gt.lesson_id == lesson_id],
            key=lambda gt: gt.order
        )
        url_slug = corpus.series[lesson.series_id].slug
        lesson_url = f"https://lrc.la.utexas.edu/eieol/{url_slug}/{lesson.order}"
        language = corpus.language[lesson.language_id].lang_attribute
        raw_html = "\n".join([gt.glossed_text for gt in glossed_texts])
        en_html = lesson.lesson_translation
        chunks = get_chunks(glossed_texts, glossed_text_to_tokens)
        section = Section(
            id=lesson_id,
            lesson_url=lesson_url,
            language=language,
            chunks=chunks,
            raw_html=raw_html,
            en_html=en_html
        )
        if len(chunks) > 0:
            n_chunks += len(chunks)
            n_sections += 1
            sections.append(section)

    print(f"Successfully parsed {n_sections} sections with {n_chunks} chunks")
    return sections


def get_chunks(
    glossed_texts: list[GlossedText],
    glossed_text_to_tokens: dict[int, list[Token]]
) -> list[Chunk]:
    """Get the chunks for a section"""
    chunks = []
    for glossed_text in glossed_texts:
        chunk = Chunk(
            id=glossed_text.id,
            text=clean_whitespace(clean_html(glossed_text.glossed_text)),
            en_text="TODO",
            tokens=glossed_text_to_tokens[glossed_text.id]
        )
        chunks.append(chunk)
    return chunks


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
    for id in corpus.glossed_text.keys():
        glosses = glossed_text_to_glosses[id]
        tokens = []
        for gloss in glosses:
            parts_of_speech = []
            for element in gloss_to_elements[gloss.id]:
                parts_of_speech.append(
                    POS(
                        part_of_speech=clean_whitespace(element.part_of_speech),
                        analysis=clean_whitespace(element.analysis)
                    )
                )
            keywords = [
                corpus.head_word[element.head_word_id].keywords
                for element in gloss_to_elements[gloss.id]
            ]
            token = Token(
                id=gloss.id,
                text=clean_whitespace(gloss.surface_form),
                parts_of_speech=parts_of_speech,
                en_text=clean_whitespace(gloss.contextual_gloss),
                en_keywords=keywords
            )
            tokens.append(token)
        id_to_tokens[id] = tokens

    return id_to_tokens
