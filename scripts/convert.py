import argparse
from dataclasses import asdict
import json
from pathlib import Path
from typing import Any
from zipfile import PyZipFile

from clean import clean_corpus
from corpus import Language, load_corpus
from sentences import Sentence, parse_sentences


def main(zip_path: Path, temp_folder: Path, final_folder: Path) -> None:
    """
    Convert a zip file that contains the LRC database dump of dead language data
    into JSON-lines files for easier use.
    """
    print(
        f"Converting data in {zip_path} to processed data in {final_folder}, using "
        f"{temp_folder} for intermediate files"
    )

    # extract contents of zip file
    extracted_files = extract(zip_path=zip_path, temp_folder=temp_folder)
    print(f"Extracted {len(extracted_files)} files to {temp_folder}:")
    for path in extracted_files:
        print(f"- {path}")

    # load the unprocessed corpus
    unprocessed_corpus = load_corpus(extracted_files)

    # clean the corpus
    cleaned_corpus = clean_corpus(unprocessed_corpus)

    # create sentences
    sentences = parse_sentences(cleaned_corpus)

    # save as JSON lines files
    save_to_final(
        final_folder=final_folder,
        sentences=sentences,
        languages=cleaned_corpus.language
    )


def extract(zip_path: Path, temp_folder: Path) -> list[Path]:
    """Extract files from the zip and return the list of files"""
    zip = PyZipFile(zip_path)
    names = zip.namelist()
    zip.extractall(temp_folder)
    return [temp_folder / name for name in names]


def save_to_final(
    final_folder: Path, sentences: list[Sentence], languages: dict[int, Language]
) -> None:
    """
    Save the sentences as JSON lines files. Create a file of all languages, as
    well as one file per langauge. Also create a data file that describes the
    languages.
    """
    # parse the date from the final folder
    date = str(final_folder).split("-")[-1]

    # save all
    all_path = final_folder / f"dlc-{date}-all.jsonl"
    write_json_lines(sentences=sentences, path=all_path)

    lang_data = []

    for language in languages.values():
        lang_path = final_folder / f"dlc-{date}-{language.lang_attribute}.jsonl"
        lang_sentences = [
            sentence for sentence in sentences
            if sentence.language == language.lang_attribute
        ]
        if len(lang_sentences) > 0:
            write_json_lines(sentences=lang_sentences, path=lang_path)
        else:
            print(
                f"Found no sentences for {language.language} ({language.lang_attribute})"
            )
        lang_data.append(
            dict(
                language=language.language,
                abbreviation=language.lang_attribute,
                n_sentences=len(lang_sentences)
            )
        )

    # write out a data file
    data_path = final_folder / f"data-dlc-{date}.json"
    data = dict(
        languages=lang_data
    )
    with open(data_path, "w") as fout:
        json.dump(data, fout)


def write_json_lines(sentences: list[Sentence], path: Path) -> None:
    """Write sentences as JSON lines"""
    print(f"Writing {len(sentences)} sentences to {path}")
    json_lines = []
    for sentence in sentences:
        line = json.dumps(asdict(sentence), ensure_ascii=False)
        json_lines.append(line)

    with open(path, "w") as fout:
        fout.writelines(json_lines)


def create_arg_parser() -> argparse.ArgumentParser:
    """Set up an argument parser to interpret the input arguments to this script"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "zip_path", type=Path, help="Location of the database dump as a zip file"
    )
    parser.add_argument(
        "temp_folder", type=Path, help="Where to store intermediate files"
    )
    parser.add_argument(
        "final_folder", type=Path, help="Where to output the final processed files"
    )
    return parser


if __name__ == "__main__":
    parser = create_arg_parser()
    args = parser.parse_args()
    main(
        zip_path=args.zip_path,
        temp_folder=args.temp_folder,
        final_folder=args.final_folder
    )
