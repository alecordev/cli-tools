import pathlib
import datetime

from concurrent.futures import ThreadPoolExecutor

import requests


def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")


def download(d):
    """Download a file from a URL

    Parameters
    ----------
    d : tuple
        First element should be the filename, second element the URL to fetch it from.
    """
    filename, url = d
    path = pathlib.Path(__file__).parent

    try:
        log(f"Starting download of {filename}")
        r = requests.get(url, stream=True)
        with open(path.joinpath(filename), "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if not chunk:
                    break
                f.write(chunk)
        log(f"{filename} downloaded.")
    except Exception as e:
        log(e)


def main():
    files_to_filter_for = []
    urls = [
        line.strip().split()
        for line in open("download.txt", "r")
        if len(line) > 10 and line.strip().split()[0] in files_to_filter_for
    ]

    with ThreadPoolExecutor() as pool:
        results = list(pool.map(download, urls))
    log("Done.")


if __name__ == "__main__":
    main()
