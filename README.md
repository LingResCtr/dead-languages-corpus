# dead-languages-corpus
Text data in a number of dead Indo-European languages from UT Austin's Linguistic Research Center (LRC)

---
YAML tags:
- TBD
---

## Dataset Description

- **Repository:** [LRC Dead Languages Corpus](https://github.com/LingResCtr/dead-languages-corpus)
- **Point of Contact:** [Todd Krause, Linguistics Research Center](bobtodd@utexas.edu)

### Dataset Summary

A data set of historical Indo-European languages, from the [Linguistics Research Center](https://liberalarts.utexas.edu/lrc/) ([LRC](https://liberalarts.utexas.edu/lrc/)) at the [University of Texas at Austin](https://www.utexas.edu/).

TBD: its intended use and the supported tasks.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Languages include: Albanian, Classical Armenian (in both original script and Romanized transliteration), Baltic (Lithuanian and Latvian), Old English, Old French, Gothic, Classical and New Testament Greek, Hittite, Old Iranian (Avestan and Old Persian), Old Irish, Latin, Old Norse, Old Russian, Vedic Sanskrit, Old Church Slavonic, Tocharian A, and Tocharian B.

The language data comes from excerpts of original documents containing prose, poetry, and biblical texts.

The [BCP-47 codes](https://www.w3.org/International/articles/bcp47/) included in this dataseta are: alb, arm, arm-Armn, bat, ang, fro, got, grc-Grek, hit-Latn, ira, sga, lat, non, rus-Cyrl, san-Latn, chu-Cyrs, xto-Latn, txb-Latn.

## Dataset Structure

The official data sets can be found in the [final](./final) directory. Within each subdirectory
of `final`, there are a number of JSON-lines files, one per language, as well as one
marked "all" which contains the data from all of the languages. The files are named
`dlc-<date>-<lang>.jsonl`. There is an additional file, named `data-dlc-<date>.json`
that contains statistics of the data sets per language.


### Data Instances

Each line contains data structured in JSON.
See [text_sample.txt](./text_sample.txt) for an example of a single line with pretty formatting for JSON.

The data on each line represents a "section" or a passage from some original source material.
Within each section there are a number of "chunks". These chunks sometimes align to sentence
boundaries, but not always. Future work is needed to make all chunks align with sentence
boundaries.
Within each chunk, there are a number of "tokens", representing the words in the chunk,
along with their English translation and parts of speech. Note that any given token might
have multiple parts of speech associated with it because there is not always a clean mapping
between the parts of speech we know today and the words used so long ago.

### Data Fields

#### Section
A section represents a passage of text from a dead language, along with translation and
other metadata useful to NLP researchers.
- id: System ID for this particular section. Maps to a lesson ID in the raw data.
- lesson_url: A URL where this section is analyzed on the LRC's website
- language: The ISO language code identifying the language that the section was originally written in
- raw\_html: The collected text of the section, with HTML tags in it that may be useful for aligning with the English text
- en\_html: The English translation of the section, with HTML tags in it that may be useful for aligning with the original language text
- chunks: A list of chunks (described below)

#### Chunk
A chunk is a string of text from a section. In many cases, a chunk is a sentence from the
section. There are some languages, however, where the chunks are broken up based on the
layout of the original text rather than at sentence boundaries.
- id: System ID for this particular text chunk. Maps to a glossed_text ID in the raw data.
- text: The text of the chunk in the original langauge.
- en\_text: Currently hardcoded to "TODO". Will eventually hold the English translation of the chunk of text.
- tokens: A list of tokens (described below)

#### Token
A token is a word, along with its English translation, its parts of speech, and other
metadata.
- id: System ID for this particular token. Maps to a gloss ID in the raw data.
- text: The text of the token in the original language.
- en\_text: Translation of the word in English.
- en\_keywords: System-internal tags applied to this token.
- parts\_of\_speech: List of POS (described below)

#### POS
- part\_of\_speech: Typically invariable grammatical features of this word. Examples include
"noun", "verb", etc.
- analysis: Grammatical information for this word that typically varies from instance to
instance. Examples include "nominative singular masculine",
"first person plural indirect object", etc. Can be null.

### Data Splits

The data is _not_ split into training and validation sets. However, it is split by language
if you would like to consume it that way. Those files look like `dlc-<date>-<lang>.jsonl`
It is also collected all together in the file named `dlc-<date>-all.jsonl`.

## Dataset Creation

### Curation Rationale

The goal of this project is to ensure that the LRC's data collection is accessible in a modern, open-source, and developer-friendly format.

### Source Data

The source data comes from the [LRC](https://liberalarts.utexas.edu/lrc/)'s [Early Indo-European OnLine](https://lrc.la.utexas.edu/eieol) ([EIEOL](https://lrc.la.utexas.edu/eieol)) collection of language lessons.

#### Initial Data Collection and Normalization

Initial data was downloaded on 2022/11/17.  The scripts included can be run on subsequent data imports collected in the `raw/` subdirectory.

To convert the data from the zip file of the database dump to the jsonl files in the
`final` folder, run `./convert.sh` from the root of this repo. The python scripts used
were developed in Python 3.10, but should work just fine in other Python 3 releases. There
are no dependencies needed besides Python and bash to run the conversion scripts.

#### Who are the source language producers?

The data was originally produced and collected by humans.

The lessons were originally compiled as part of a broader education project. Authors were scholars working at or with the University of Texas at Austin.

### Annotations

[More Information Needed]

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

The authors of the texts have been dead for a millenium, and as such the dataset does not contain what we would consider PII.

## Considerations for Using the Data

### Social Impact of Dataset

TBD: [More Information Needed]

### Discussion of Biases

The data represents societies from eras when sexism, racism, and ableism were the norm, and this may be reflected in a given dataset.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The texts were originally compiled by a variety of authors working at or with the University of Texas, including: Brigitte L.M. Bauer, Angelo Costanz, Scott Harvey, Brian Joseph, Todd B. Krause, Winfred P. Lehmann, Jonathan Slocum, Sandra B. Straubhaar, Patrizia de Bernardo Stempel, Virginija Vasiliauskiene, and Lilita Zalkalns.

Todd Krause, Amanda Krauss, and Shayne Miel collaborated on the publication to GitHub.

The original work was carried out under grants from the Salus Mundi Foundation, for which we owe thanks to Dr. A. Richard Diebold, Jr.

### Licensing Information

The data is licensed under [Creative Commons 4.0 Non-Commercial](https://creativecommons.org/licenses/by-nc/4.0/legalcode).

The processing scripts are licensed under [MIT](https://opensource.org/licenses/MIT).

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@fraglegs](https://github.com/<fraglegs>) for adding this dataset.
