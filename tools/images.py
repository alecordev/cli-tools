"""
Create listings of images from a tree based on filters.

Copy them to given locations. Allow processing with Pillow - use case is to resize and reduce space.
"""

import os
import pathlib

from concurrent.futures import ProcessPoolExecutor

from PIL import Image


def copy_opt(source):
    original = Image.open(source)

    dest = os.path.join(r'R:\Fotos', source.stem + '.jpg')
    factor = 1
    width_original, height_original = original.size
    width = int(width_original * factor)
    height = int(height_original * factor)
    new = original.resize((width, height), Image.ANTIALIAS)
    new.save(dest)
    print(f'{source} saved as {dest}')


def main():
    tree_source = r'Photos/Source'
    destination_path = r'Photos/Destination'
    os.makedirs(destination_path, exist_ok=True)
    images = (f for f in pathlib.Path(tree_source).rglob('*.jpg') if '2018' in str(f))
    with ProcessPoolExecutor() as pool:
        pool.map(copy_opt, images)
    # with ProcessPoolExecutor() as pool:
    #     pool.map(copy_opt, f, os.path.join(destination_path, f.stem + '.jpg'))
    # for f in images:
    #     copy_opt(f, os.path.join(destination_path, f.stem + '.jpg'))


if __name__ == '__main__':
    print('Starting execution')
    main()
