import sys
import pathlib


def main(path):
    p = pathlib.Path(path)
    names = [
        line.strip().split()[0] for line in open("download.txt", "r") if len(line) > 10
    ]
    files_in_directory = {f.name for f in p.glob("*.zip") if f.is_file()}
    print(
        f"Quantity of files in source: {len(names)}. Quantity of files in directory: {len(files_in_directory)}"
    )
    print("Difference:")
    print(files_in_directory.symmetric_difference(names))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Path must be provided as first parameter")
    main(sys.argv[1])
