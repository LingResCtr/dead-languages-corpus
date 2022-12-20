import re

from corpus import Corpus, GlossedText


def clean_corpus(corpus: Corpus) -> Corpus:
    """
    Do all cleaning steps on the data before we start to put it into the final structure
    """
    print("Removing stray HTML from glossed_text")
    corpus.glossed_text = clean_html(corpus.glossed_text)

    print("Condensing whitespace in glossed_text")
    corpus.glossed_text = clean_whitespace(corpus.glossed_text)

    return corpus


def clean_html(glossed_text: dict[int, GlossedText]) -> dict[int, GlossedText]:
    """
    There is a lot of stray HTML in the glossed text. However, some of it is
    semantically important. This function removes the pieces that do not affect the
    meaning of the text.

    See the "Cleaning HTML.ipynb" notebook for more information.
    """
    br = re.compile("<br ?/?> ?")
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


def clean_whitespace(glossed_text: dict[int, GlossedText]) -> dict[int, GlossedText]:
    """
    Replace new lines with \\n and otherwise convert all consecutive whitespace to a
    single space. Run this after clean_html() for best results with <br> tags, etc
    """
    newline = re.compile(r"\s*\n\s*")
    whitespace = re.compile(r"\s+")

    ret = {}
    for id, row in glossed_text.items():
        text = row.glossed_text.strip()
        text = newline.sub("\\n", text)
        text = whitespace.sub(" ", text)

        row.glossed_text = text
        ret[id] = row

    return ret
