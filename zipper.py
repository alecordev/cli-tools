import os
import sys
import argparse
import zipfile
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='[%(asctime)s] - PID: %(process)d - TID: %(thread)d - %(levelname)s - %(message)s')


def zip_dir(output_filename, directory_to_compress):
    """
    Makes a zip file from a given directory (and all its tree)
    """
    try:
        relroot = os.path.abspath(os.path.join(
            directory_to_compress, os.pardir))
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(directory_to_compress):
                # add directory (needed for empty dirs)
                z.write(root, os.path.relpath(root, relroot))
                for file in files:
                    try:
                        filename = os.path.join(root, file)
                        if os.path.isfile(filename):  # regular files only
                            arcname = os.path.join(
                                os.path.relpath(root, relroot), file)
                            z.write(filename, arcname)
                    except Exception as e:
                        logging.exception(e)
                        continue
            logging.info('Finished creating {}'.format(output_filename))
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version='0.1')
        parser.add_argument(
            '-o', '--output', metavar=('OUTPUT'), help='Output filename')
        parser.add_argument('-d', '--directory',
                            metavar=('DIRECTORY'), help='Directory to zip')
        args = parser.parse_args()

        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(0)

        zip_dir(args.output, args.directory)

    except Exception as e:
        logging.exception(e)
