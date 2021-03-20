"""
File format YYYY-MM-###...
Create directory if it does not exist
Move all files matching that same pattern to the directory
"""
import sys
import pathlib


def main(path):
    p = pathlib.Path(path)
    files = [f for f in p.glob("*.zip") if f.is_file()]
    for f in files:
        d = f.name[:7]
        t = f.name[8:11]
        p.joinpath(t, d).mkdir(parents=True, exist_ok=True)
        f.replace(p.joinpath(t, d, f.name))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Path must be provided as first parameter")
    main(sys.argv[1])
