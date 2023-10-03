"""
Given 2 paths, compare them.
Use filename and size.
Define which should be the superset. Ignores structure, unless you want to use relative_path.
"""

import json
from pathlib import Path


def list_files_and_sizes_with_relative_path(path):
    file_info = {}
    for file_path in path.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(path)
            file_info[str(relative_path)] = file_path.stat().st_size
    return file_info


def list_files_and_sizes_only_filenames(path):
    file_info = {}
    for file_path in path.rglob("*"):
        if file_path.is_file():
            file_info[file_path.name] = file_path.stat().st_size
    return file_info


def compare_paths(path1, path2, path1_is_superset=True):
    path1 = Path(path1)
    path2 = Path(path2)

    files_and_sizes1 = list_files_and_sizes_only_filenames(path1)
    files_and_sizes2 = list_files_and_sizes_only_filenames(path2)

    if path1_is_superset:
        # Find files unique to path2
        unique_to_path2 = set(files_and_sizes2.keys()) - set(files_and_sizes1.keys())
        return {f'Files unique to {path2}': unique_to_path2}
    else:
        # Find files unique to path1
        unique_to_path1 = set(files_and_sizes1.keys()) - set(files_and_sizes2.keys())
        return {f'Files unique to {path1}': unique_to_path1}


if __name__ == "__main__":
    path1 = input("Enter the first path: ")
    path2 = input("Enter the second path: ")
    path1_is_superset = input(
        "Is the first path the superset (contains all files of the second path)? (y/n): "
    ).lower()

    if path1_is_superset == 'y':
        path1_is_superset = True
    else:
        path1_is_superset = False

    if Path(path1).exists() and Path(path2).exists():
        result = compare_paths(path1, path2, path1_is_superset)
        print("\nComparison Result:")
        for key, value in result.items():
            print(key)
            report = json.dumps(list(value))
            print(report)
            with open(f'report.json', 'w') as f:
                f.write(report)
    else:
        print("One or both paths do not exist.")
