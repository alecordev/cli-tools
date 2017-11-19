""" Print a directory tree """

import os
import sys


def directory_tree(path, show_files=True, indentation=4, file_output=False):
    """
    Shows the contents of a directory in a tree structure.

    Arguments
    ---------
    path (string): path of the root folder we want to show.
    show_files (boolean): Whether or not we want to see files listed.
                            Defaults to False.
    indentation (int): Indentation we want to use, defaults to 2.
    file_output (string): Path (including the name) of the file where we want
                            to save the tree.
    """

    tree = []

    if not show_files:
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * indentation * (level)
            tree.append('{}{}/'.format(indent, os.path.basename(root)))

    if show_files:
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * indentation * (level)
            tree.append('{}{}/'.format(indent, os.path.basename(root)))
            for f in files:
                subindent = ' ' * indentation * (level + 1)
                tree.append('{}{}'.format(subindent, f))

    if file_output:
        output_file = open(file_output, 'w')
        for line in tree:
            output_file.write(line)
            output_file.write('\n')
    else:
        # Default behaviour: print on screen.
        for line in tree:
            print(line)


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            directory_tree(sys.argv[1])
        else:
            directory_tree(os.path.dirname(os.path.abspath(__name__)))
    except Exception as e:
        print(e)
