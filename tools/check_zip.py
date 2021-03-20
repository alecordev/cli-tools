import sys
import pathlib
import zipfile

from concurrent.futures import ProcessPoolExecutor


def check_file(f):
    try:
        zipped = zipfile.ZipFile(f)
        result = zipped.testzip()
    except Exception as e:
        print(f"Error processing {f} - {e}")
    else:
        print(f"{f} ok.")


def main(path: pathlib.Path = None):
    if not path:
        raise Exception("Path is mandatory")

    files = (f for f in path.glob("*.zip") if f.is_file())
    with ProcessPoolExecutor() as pool:
        results = [
            res for res in pool.map(check_file, files, chunksize=1) if res is not None
        ]

    # with open("zipped_report.txt", "w") as f:
    #     f.write("\n".join(results))
    # print(results)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Need to provide PATH as parameter")
        sys.exit(1)

    main(pathlib.Path(sys.argv[1]))
