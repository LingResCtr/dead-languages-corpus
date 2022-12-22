import argparse
from dataclasses import asdict
import json
from pathlib import Path
from zipfile import PyZipFile

from corpus import Language, load_corpus
from sections import Section, parse_sections


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
    corpus = load_corpus(extracted_files)

    # create sentences
    sections = parse_sections(corpus)

    # save as JSON lines files
    save_to_final(
        final_folder=final_folder,
        sections=sections,
        languages=corpus.language
    )


def extract(zip_path: Path, temp_folder: Path) -> list[Path]:
    """Extract files from the zip and return the list of files"""
    zip = PyZipFile(zip_path)
    names = zip.namelist()
    zip.extractall(temp_folder)
    return [temp_folder / name for name in names]


def save_to_final(
    final_folder: Path, sections: list[Section], languages: dict[int, Language]
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
    write_json_lines(sections=sections, path=all_path)

    lang_stats = []

    for language in languages.values():
        lang_path = final_folder / f"dlc-{date}-{language.lang_attribute}.jsonl"
        lang_sections = [
            section for section in sections
            if section.language == language.lang_attribute
        ]

        stats = dict(
            language=language.language,
            abbreviation=language.lang_attribute,
            n_sections=len(lang_sections),
            n_chunks=sum([len(section.chunks) for section in lang_sections])
        )
        if stats["n_sections"] > 0:
            print(
                f"Writing {stats['n_sections']} sections "
                f"with {stats['n_chunks']} chunks "
                f"to {lang_path}"
            )
            write_json_lines(sections=lang_sections, path=lang_path)
        else:
            print(
                f"Found no sections for {language.language} ({language.lang_attribute})"
            )
        lang_stats.append(stats)

    # write out a data file
    data_path = final_folder / f"data-dlc-{date}.json"
    data = dict(
        languages=lang_stats
    )
    with open(data_path, "w") as fout:
        json.dump(data, fout)


def write_json_lines(sections: list[Section], path: Path) -> None:
    """
    Write instances as JSON lines

    The elements of the `instances` list must all be dataclasses
    """
    json_lines = []
    for section in sections:
        line = json.dumps(asdict(section), ensure_ascii=False)
        json_lines.append(line)

    with open(path, "w") as fout:
        fout.write("\n".join(json_lines))


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
