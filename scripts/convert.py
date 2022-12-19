import argparse
from pathlib import Path


def main(zip_path: Path, temp_folder: Path, final_folder: Path) -> None:
    """
    Convert a zip file that contains the LRC database dump of dead language data
    into JSON-lines files for easier use.
    """
    print(
        f"Converting data in {zip_path} to processed data in {final_folder}, using "
        f"{temp_folder} for intermediate files"
    )


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
