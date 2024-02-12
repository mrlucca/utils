import os
import sys
import time
import argparse
from typing import Tuple, Callable

minimal_version = (3, 12)

if sys.version_info < minimal_version:
    raise RuntimeError("minimal version is not satisfied")
    
FILE_STRATEGIES = {
    "SQLITE": ( 
        b"\x53\x51\x4c\x69\x74\x65\x20\x66\x6f\x72\x6d\x61\x74\x20\x33\x00",
        16,
    ),
}

EXPORT_RESULT_STRATEGIES = {
    "TXT": ...,
    "SQLITE": ...,
}


def factory_check_magic_bytes_from(magic_bytes: bytes, read_size: int) -> Callable[[str], bool]:
    
    def check_magic_bytes_callback(path: str) -> str | None:
        if not os.path.exists(path):
            return
        
        try:
            with open(path, 'rb') as file:
                header = file.read(read_size) 
        except (PermissionError, OSError):
            # TODO add log
            return False
        else:
            return header.startswith(magic_bytes)
        
    return check_magic_bytes_callback
    

def get_file_info(path: str) -> Tuple[float, str, str]:
    size_in_bytes = os.path.getsize(path)
    size_in_mb = size_in_bytes / (1024 * 1024)

    modification_time = os.path.getmtime(path)
    creation_time = os.path.getctime(path)

    modification_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modification_time))
    creation_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))
    return size_in_mb, creation_date, modification_date


def scan_filers(path: str, check_magic_bytes_cb: Callable[[str], bool]):
    for root, _, filers in os.walk(path):
        is_empty = len(filers) == 0
        
        if is_empty:
            continue

        for file_path in filers:
            current_path = os.path.join(root, file_path)

            if not check_magic_bytes_cb(current_path):
                continue
            
            size_in_mb, created_at, modified_at = get_file_info(current_path)
            print((
                current_path,
                size_in_mb,
                created_at,
                modified_at
            ))
            


def setup_and_run_scan_filers(path: str, file_strategy: str | None, export_result: str):
    global FILE_STRATEGIES
    file_strategy_resp = FILE_STRATEGIES.get(file_strategy)
    file_strategy_exists = file_strategy_resp is not None
    assert file_strategy_exists, f"file strategy not found {file_strategy}. You can try {','.join(FILE_STRATEGIES.keys())}"
    export_result_strategy_resp = EXPORT_RESULT_STRATEGIES.get(export_result)
    export_result_strategy_exists = export_result_strategy_resp is not None
    assert export_result_strategy_exists, f"export result strategy not found {export_result}. You can try {','.join(EXPORT_RESULT_STRATEGIES.keys())}"
    magic_bytes, read_size = file_strategy_resp
    check_magic_bytes_cb = factory_check_magic_bytes_from(magic_bytes, read_size)
    scan_filers(path, check_magic_bytes_cb)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to scan files, from magic bytes')
    parser.add_argument('path', metavar='PATH', type=str, nargs='?', default=os.getcwd(), help='Path to the directory to be scanned (default: current directory)')
    parser.add_argument('--file-strategy', metavar='FILE_STRATEGY', type=str, help='Strategy to scan the files: e.g.: SQLITE')
    parser.add_argument('--export-result', metavar='EXPORT_RESULT', type=str, default="TXT", help='Export result e.g.: SQLITE, TXT,  (default: TXT)')
    args = parser.parse_args()
    setup_and_run_scan_filers(args.path, args.file_strategy, args.export_result)