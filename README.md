# dead-languages-corpus
Text data in a number of dead Indo-European languages from UT Austin's Linguistic Research Center

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

Each line contains data structured in JSON.  See [text_sample.txt](./text_sample.txt) for an example of a single line with pretty formatting for JSON.

### Data Instances

[More Information Needed]

### Data Fields

---
 id: "system ID for this particular text chunk"
 language: "ISO language code"
 text: "chunk of text in the target language"
 en\_text: (?... not sure yet)
 tokens: "list of individual tokens in the text chunk (in JSON)"

---
 tokens:
   - text: "the specific string glossed from the text chunk"
   - parts\_of\_speech: "list of elements of grammatical analysis (in JSON)"
   - en\_text: "translation of the text in English"
   - en\_keywords: "system-internal tags applied to this token"

---
parts\_of\_speech:
  - part\_of\_speech: "typically invariable grammatical features of this word"
  - analysis: "grammatical information for this word that typical varies from instance to instance"

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

The goal of this project is to ensure that the LRC's data collection is accessible in a modern, open-source, and developer-friendly format.

### Source Data

The source data comes from the [LRC](https://liberalarts.utexas.edu/lrc/)'s [Early Indo-European OnLine](https://lrc.la.utexas.edu/eieol) ([EIEOL](https://lrc.la.utexas.edu/eieol)) collection of language lessons.

#### Initial Data Collection and Normalization

Initial data was downloaded on 2022/11/17.  The scripts included can be run on subsequent data imports collected in the `raw/` subdirectory.

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
