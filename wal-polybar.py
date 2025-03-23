#!/usr/bin/python3
import os
import sys
from os.path import join

VERSION = '0.9'
HOME = os.getenv('HOME')
POLYBAR_CONFIG_FOLDER_PATH = join(HOME, '.config/polybar/')
POLYBAR_CONFIG_PATH = join(POLYBAR_CONFIG_FOLDER_PATH, 'config')
POLYBAR_TEMPLATE_PATH = join(POLYBAR_CONFIG_FOLDER_PATH, 'config.template')
WAL_CACHE_PATH = join(HOME, '.cache/wal/colors')

def wal_cache_file_to_dict():
    """Load the pywal colors from the cache file and return a list of placeholder/color tuples."""
    try:
        with open(WAL_CACHE_PATH, 'r') as file:
            colors = []
            for index, line in enumerate(file.readlines()):
                # Remove any trailing whitespace/newline characters
                colors.append(('${{wal.color{}}}'.format(index), line.strip()))
    except IOError as e:
        print('Error reading WAL cache file ({}): {}'.format(WAL_CACHE_PATH, e))
        sys.exit(1)
    return colors

def modify_polybar_config_file(colors):
    """Replace placeholders in the polybar template with colors from pywal and write the new config."""
    try:
        with open(POLYBAR_TEMPLATE_PATH, 'r') as template_file:
            template_lines = template_file.readlines()
    except IOError as e:
        print('Error reading the Polybar template file ({}): {}'.format(POLYBAR_TEMPLATE_PATH, e))
        sys.exit(1)

    try:
        with open(POLYBAR_CONFIG_PATH, 'w') as config_file:
            for line in template_lines:
                for placeholder, color in colors:
                    if placeholder in line:
                        line = line.replace(placeholder, color)
                config_file.write(line)
    except IOError as e:
        print('Error writing the Polybar config file ({}): {}'.format(POLYBAR_CONFIG_PATH, e))
        sys.exit(1)

def main():
    global POLYBAR_TEMPLATE_PATH, WAL_CACHE_PATH, VERSION

    # Handle command-line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v':
            print('wal-polybar ' + VERSION)
            sys.exit(0)
        elif sys.argv[1] in ['-h', '--help']:
            print("Usage: wal-polybar [-h] [-v] [-t 'path/to/template']\n")
            print("Optional arguments:")
            print("\t-h, --help   Show this help message and exit")
            print("\t-v           Display the version of wal-polybar")
            print("\t-t           Use a custom template for polybar")
            sys.exit(0)
        elif '-t' in sys.argv:
            t_index = sys.argv.index('-t')
            if t_index + 1 < len(sys.argv):
                POLYBAR_TEMPLATE_PATH = sys.argv[t_index + 1]
                if not os.path.isfile(POLYBAR_TEMPLATE_PATH):
                    print('The provided template file does not exist: {}'.format(POLYBAR_TEMPLATE_PATH))
                    sys.exit(1)
            else:
                print("Missing template path after -t")
                sys.exit(1)
        else:
            print('Syntax error!')
            sys.exit(1)

    # Check if the WAL cache file exists
    if not os.path.isfile(WAL_CACHE_PATH):
        print('Could not find the WAL cache file at {}.'.format(WAL_CACHE_PATH))
        print('Please run pywal to generate the colors file.')
        sys.exit(1)

    print('Loading wal cache...')
    colors = wal_cache_file_to_dict()
    print('Wal cache successfully loaded!')
    print('Loading the template and generating the new config...')
    modify_polybar_config_file(colors)
    print('Template file successfully loaded and new config file generated!')

if __name__ == '__main__':
    main()
