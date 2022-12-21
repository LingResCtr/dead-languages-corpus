from dataclasses import fields
import re
from typing import Any

from corpus import Corpus, GlossedText


def clean_corpus(corpus: Corpus) -> Corpus:
    """
    Do all cleaning steps on the data before we start to put it into the final structure
    """
    print("Removing stray HTML from glossed_text")
    corpus.glossed_text = clean_html(corpus.glossed_text)

    print("Condensing whitespace in corpus")
    corpus = clean_all_whitespace(corpus)

    return corpus


def clean_html(glossed_text: dict[int, GlossedText]) -> dict[int, GlossedText]:
    """
    There is a lot of stray HTML in the glossed text. However, some of it is
    semantically important. This function removes the pieces that do not affect the
    meaning of the text.

    See the "Cleaning HTML.ipynb" notebook for more information.
    """
    br = re.compile("<br ?/?>")
    line_number = re.compile("^<((font[^<]+</font>)|(i[^<]+</i>)) (- )?")
    omit = re.compile("\[<i[^<]+omitted[^>]+>\]")
    p = re.compile("^[^<]+<p>[^)]+\) ")
    close_p = re.compile("</p>")
    div = re.compile("</?div>")

    ret = {}
    for id, row in glossed_text.items():
        text = row.glossed_text
        text = line_number.sub("", text)
        text = br.sub("", text)
        text = omit.sub("", text)
        text = p.sub("", text)
        text = close_p.sub("", text)
        text = div.sub("", text)

        row.glossed_text = text
        ret[id] = row

    return ret


def clean_all_whitespace(corpus: Corpus) -> Corpus:
    """
    Replace new lines with \\n and otherwise convert all consecutive whitespace to a
    single space. Run this after clean_html() for best results with <br> tags, etc
    """
    out_corpus = {}
    for field in fields(Corpus):
        part = getattr(corpus, field.name)

        for id, row in part.items():
            for attr in fields(row.__class__):
                value = getattr(row, attr.name)
                if isinstance(value, str):
                    setattr(part[id], attr.name, clean_whitespace(value))

        out_corpus[field.name] = part
    return Corpus(**out_corpus)


def clean_whitespace(text: str):
    text = text.strip()
    text = re.sub(r"\s*\n\s*", "\\n", text)
    text = re.sub("&nbsp;", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text
