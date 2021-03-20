import sys
import pathlib
import zipfile
import multiprocessing

from concurrent.futures import ProcessPoolExecutor


def uncompress(arg):
    f, target_dir = arg
    with zipfile.ZipFile(f, "r") as zip_ref:
        target_dir.mkdir(exist_ok=True)
        zip_ref.extractall(target_dir)
    print(f"{f} unzipped in {target_dir} successfully.")


def main(path: pathlib.Path = None):
    if not path:
        raise Exception("Path is mandatory")

    files = (
        (f, f.parent.joinpath("xml"))
        for f in path.rglob("*.zip")
        if f.is_file() and f.name.startswith("2020-10")
    )
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count() // 4) as pool:
        results = list(pool.map(uncompress, files, chunksize=1))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Need to provide PATH as parameter")
        sys.exit(1)

    main(pathlib.Path(sys.argv[1]))
