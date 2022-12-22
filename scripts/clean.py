import re
from typing import Optional


def clean_html(text: str) -> str:
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

    text = line_number.sub("", text)
    text = br.sub("", text)
    text = omit.sub("", text)
    text = p.sub("", text)
    text = close_p.sub("", text)
    text = div.sub("", text)

    return text


def clean_whitespace(text: Optional[str]):
    if isinstance(text, str):
        text = text.strip()
        text = re.sub(r"\s*\n\s*", "\n", text)
        text = re.sub("&nbsp;", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
    return text
