from dataclasses import dataclass
import re

from clean import clean_whitespace
from corpus import Corpus, GlossedText


@dataclass
class Translation:
    language: str
    lesson_id: int
    original: str
    english: str


def extract_translations(corpus: Corpus) -> list[Translation]:
    """
    Extract the original text and English translations from the Lesson texts

    Attempt to find this data with using beautiful soup to avoid having to deal with
    dependencies
    """
    translations = []

    for lesson in corpus.lesson.values():
        if lesson.lesson_translation is None:
            continue

        original_html = get_lesson_text_html(
            glossed_text=corpus.glossed_text,
            lesson_id=lesson.id
        )
        english_html = lesson.lesson_translation

        translations.append(
            Translation(
                language=corpus.language[lesson.language_id].lang_attribute,
                lesson_id=lesson.id,
                original=original_html,
                english=english_html
            )
        )

    return translations


def get_lesson_text_html(glossed_text: dict[int, GlossedText], lesson_id: int) -> str:
    """Combine the glossed texts for this lesson"""
    lesson_texts = [gt for gt in glossed_text.values() if gt.lesson_id == lesson_id]
    lesson_texts.sort(key=lambda gt: gt.order)

    return " ".join([lt.glossed_text for lt in lesson_texts])
