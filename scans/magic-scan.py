import os
import argparse


def scan_filers(path: str, file_strategy: str, export_result: str):
    print(path, file_strategy, export_result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to scan files, from magic bytes')
    parser.add_argument('path', metavar='PATH', type=str, nargs='?', default=os.getcwd(), help='Path to the directory to be scanned (default: current directory)')
    parser.add_argument('--file-strategy', metavar='FILE_STRATEGY', type=str, help='Strategy to scan the files: e.g.: SQLITE')
    parser.add_argument('--export-result', metavar='EXPORT_RESULT', type=str, default="TXT", help='Export result e.g.: SQLITE, TXT')
    args = parser.parse_args()


    scan_filers(args.path, args.file_strategy, args.export_result)