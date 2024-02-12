import os
import sys
import argparse


minimal_version = (3, 12)


if sys.version_info < minimal_version:
    raise RuntimeError("minimal version is not satisfied")


FILE_STRATEGIES = {
    "SQLITE": ...,
}

EXPORT_RESULT_STRATEGIES = {
    "TXT": ...,
    "SQLITE": ...,
}

def scan_filers(path: str, file_strategy: str | None, export_result: str):
    global FILE_STRATEGIES
    file_strategy_exists = FILE_STRATEGIES.get(file_strategy) is not None
    assert file_strategy_exists, f"file strategy not found {file_strategy}. You can try {','.join(FILE_STRATEGIES.keys())}"
    export_result_strategy_exists = EXPORT_RESULT_STRATEGIES.get(export_result) is not None
    assert export_result_strategy_exists, f"export result strategy not found {export_result}. You can try {','.join(EXPORT_RESULT_STRATEGIES.keys())}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to scan files, from magic bytes')
    parser.add_argument('path', metavar='PATH', type=str, nargs='?', default=os.getcwd(), help='Path to the directory to be scanned (default: current directory)')
    parser.add_argument('--file-strategy', metavar='FILE_STRATEGY', type=str, help='Strategy to scan the files: e.g.: SQLITE')
    parser.add_argument('--export-result', metavar='EXPORT_RESULT', type=str, default="TXT", help='Export result e.g.: SQLITE, TXT,  (default: TXT)')
    args = parser.parse_args()


    scan_filers(args.path, args.file_strategy, args.export_result)