import sys
import pathlib
import subprocess

HERE = pathlib.Path(__file__).parent

dirs = [e for e in HERE.iterdir() if e.is_dir()]
print(dirs)

for e in dirs:
    subprocess.run("git pull", shell=True, cwd=e, stdout=sys.stdout)
