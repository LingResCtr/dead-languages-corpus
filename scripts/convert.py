import argparse
from pathlib import Path
from zipfile import PyZipFile

from corpus import load_corpus


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


def extract(zip_path: Path, temp_folder: Path) -> list[Path]:
    """Extract files from the zip and return the list of files"""
    zip = PyZipFile(zip_path)
    names = zip.namelist()
    zip.extractall(temp_folder)
    return [temp_folder / name for name in names]


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
