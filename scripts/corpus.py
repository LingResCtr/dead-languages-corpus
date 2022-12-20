from abc import ABC, abstractstaticmethod
import csv
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Optional, Type, get_args


def str_or_none(s: str) -> Optional[str]:
    return None if len(s) == 0 else s


def int_or_none(s: str) -> Optional[int]:
    return None if s == "NULL" else int(s)


class CorpusRow(ABC):
    @abstractstaticmethod
    def from_row(row: list[str]):
        pass


@dataclass
class Element(CorpusRow):
    """Extra info for the token"""
    id: int
    gloss_id: int            # references a Gloss
    part_of_speech: str      # the part of speech of the word
    analysis: Optional[str]  # extra info about the part of speech
    head_word_id: int        # references the HeadWord class
    order: int               # Glosses are sometimes split into two elements

    @staticmethod
    def from_row(row: list[str]) -> "Element":
        return Element(
            id=int(row[0]),
            gloss_id=int(row[1]),
            part_of_speech=row[2],
            analysis=str_or_none(row[3]),
            head_word_id=int(row[4]),
            order=int(row[5]),
        )


@dataclass
class Gloss(CorpusRow):
    """Represents a "word" in a sentence"""
    id: int
    surface_form: str                   # a word from a sentence in the glossed text
    contextual_gloss: str               # the English equivalent of the word
    comments: Optional[str]             # a comment about the translation
    underlying_form: Optional[str]      # root of the word
    language_id: int                    # maps to Language class
    glossed_text_id: Optional[int]      # maps to GlossedText class
    order: Optional[int]                # order of the word in the sentence (GlossedText)

    @staticmethod
    def from_row(row: list[str]) -> "Gloss":
        return Gloss(
            id=int(row[0]),
            surface_form=row[1],
            contextual_gloss=row[2],
            comments=str_or_none(row[3]),
            underlying_form=str_or_none(row[4]),
            language_id=int(row[5]),
            glossed_text_id=int_or_none(row[10]),
            order=int_or_none(row[11]),
        )


@dataclass
class GlossedText(CorpusRow):
    """Represents a "sentence" in the dead language"""
    id: int
    lesson_id: int      # the Lessson that this sentence is displayed in
    glossed_text: str   # the HTML-friendly text of the sentence in the lesson
    order: int          # the order in which the sentence is displayed in the lesson

    @staticmethod
    def from_row(row: list[str]) -> "GlossedText":
        return GlossedText(
            id=int(row[0]),
            lesson_id=int(row[1]),
            glossed_text=row[2],
            order=int(row[3]),
        )


@dataclass
class Grammar(CorpusRow):
    """Grammar lessons presented as part of the online lessons"""
    id: int
    lesson_id: int       # references the Lesson class
    title: str           # name of the grammar lesson
    order: int           # the order the lesson appears on the site
    grammar_text: str    # HTML version of the grammar lesson
    section_number: str  # ???

    @staticmethod
    def from_row(row: list[str]) -> "Grammar":
        return Grammar(
            id=int(row[0]),
            lesson_id=int(row[1]),
            title=row[2],
            order=int(row[3]),
            grammar_text=row[4],
            section_number=row[5],
        )


@dataclass
class HeadWord(CorpusRow):
    id: int
    word: str                 # a word form
    definition: str           # the English equivalent of the word
    language_id: int          # the id of the language (references the Language class)
    etyma_id: Optional[int]   # ???
    keywords: list[str]       # normalized English equivalents of the word

    @staticmethod
    def from_row(row: list[str]) -> "HeadWord":
        return HeadWord(
            id=int(row[0]),
            word=row[1],
            definition=row[2],
            language_id=int(row[3]),
            etyma_id=int_or_none(row[4]),
            keywords=row[9].split(","),
        )


@dataclass
class Language(CorpusRow):
    id: int
    language: str                           # the name of the language
    custom_keyboard_layout: Optional[str]   # info for mapping characters
    substitutions: Optional[str]            # info for mapping characters
    custom_sort: str                        # info for mapping characters
    lang_attribute: str                     # abbreviation for the language

    @staticmethod
    def from_row(row: list[str]) -> "Language":
        return Language(
            id=int(row[0]),
            language=row[1],
            custom_keyboard_layout=str_or_none(row[2]),
            substitutions=str_or_none(row[2]),
            custom_sort=row[4],
            lang_attribute=row[5],
        )


@dataclass
class Lesson(CorpusRow):
    """The lesson presented online. Contains the full translation of the glossed texts"""
    id: int
    series_id: int                      # references a Series object
    title: str                          # title of the lesson - identifies the source of the text
    order: int                          # the order in which the lesson appears on the site
    language_id: int                    # references the Language class
    intro_text: Optional[str]           # description of the lesson
    lesson_translation: Optional[str]   # English translation of the sentences

    @staticmethod
    def from_row(row: list[str]) -> "Lesson":
        return Lesson(
            id=int(row[0]),
            series_id=int(row[1]),
            title=row[2],
            order=int(row[3]),
            language_id=int(row[4]),
            intro_text=str_or_none(row[5]),
            lesson_translation=str_or_none(row[6]),
        )


@dataclass
class Series(CorpusRow):
    """Description of an online language course at https://liberalarts.utexas.edu/lrc/"""
    id: int
    title: str              # name of the course
    slug: str               # abbreviation for the course
    order: int              # order it appears on the site
    menu_name: str          # name as it appears in the menu
    menu_order: int         # order it appears in the menu
    expanded_title: str     # more descriptive title for the course
    published: bool         # whether it has been published yet

    @staticmethod
    def from_row(row: list[str]) -> "Series":
        return Series(
            id=int(row[0]),
            title=row[1],
            slug=row[2],
            order=int(row[3]),
            menu_name=row[4],
            menu_order=int(row[5]),
            expanded_title=row[6],
            published=row[7] == "1",
        )


@dataclass
class Corpus:
    element: dict[int, Element]
    gloss: dict[int, Gloss]
    glossed_text: dict[int, GlossedText]
    grammar: dict[int, Grammar]
    head_word: dict[int, HeadWord]
    language: dict[int, Language]
    lesson: dict[int, Lesson]
    series: dict[int, Series]


def load_corpus(csv_files: list[Path]) -> Corpus:
    """Load the corpus from a list of CSV files"""
    # create a map from the corpus part name to the type of its rows
    corpus_parts = {f.name: get_args(f.type)[1] for f in fields(Corpus)}
    parts = {}

    # for each extracted
    for file in csv_files:
        for part, row_type in corpus_parts.items():
            if file.stem.endswith(part):
                print(f"Parsing {part}")
                parts[part] = load_corpus_part(row_type, file)
                continue

    return Corpus(**parts)


def load_corpus_part(row_type: Type[CorpusRow], path: Path) -> dict[int, CorpusRow]:
    """Read a CSV file and return a list of rows, parsed as the expected type"""
    header = None
    rows = {}

    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for csv_row in reader:
            if header is None:
                header = csv_row
            else:
                assert len(header) == len(csv_row)
                corpus_row = row_type.from_row(csv_row)
                rows[corpus_row.id] = corpus_row

    return rows
