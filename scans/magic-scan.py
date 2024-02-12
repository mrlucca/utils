import os, sys, time
from typing import Self, Tuple, Callable, Protocol, runtime_checkable

assert not ( sys.version_info < (3, 12) ), "minimal python version is not satisfied"

TIME_CONSTRAINT = "%Y-%m-%d %H:%M:%S"
MAGIC_FILE_STRATEGIES = {
    "SQLITE": (b"\x53\x51\x4c\x69\x74\x65\x20\x66\x6f\x72\x6d\x61\x74\x20\x33\x00", 16),
}
global_export_result_strategies = {}         


@runtime_checkable
class ExportStrategy(Protocol):
    def __enter__(self) -> Self: ...
    def __exit__(self): ...
    def push_result(self, result: tuple): ...


class ExportCSVStrategy(ExportStrategy):
    def __init__(self):
        self._path = os.path.join(os.getcwd(), "export_result.csv")
        self._file = None

    def __enter__(self):
        self._file = open(self._path, "w+")
        self._file.write("current_path;size_in_mb;created_at;modified_at\n")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): self._file.close()
    def push_result(self, rt: tuple): self._file.write(f"{rt[0]};{rt[1]};{rt[2]};{rt[3]}\n")


class ExportSQLITEStrategy(ExportStrategy):
    def __init__(self):
        self._path = os.path.join(os.getcwd(), "export_result.db")
        self._conn = None
        self._cursor = None

    def __enter__(self):
        import sqlite3

        self._conn = sqlite3.connect(self._path)
        self._cursor = self._conn.cursor()
        self._cursor.execute('CREATE TABLE IF NOT EXISTS filers (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, size_mb REAL, creation_date DATE, modification_date DATE)')
        self._conn.commit()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): 
        self._conn.commit()
        self._conn.close()

    def push_result(self, rt: tuple): self._conn.execute(
        "INSERT INTO filers (path, size_mb, creation_date, modification_date) VALUES (?, ?, ?, ?)", rt)


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
    modification_date = time.strftime(TIME_CONSTRAINT, time.localtime(modification_time))
    creation_date = time.strftime(TIME_CONSTRAINT, time.localtime(creation_time))
    return size_in_mb, creation_date, modification_date


def scan_filers(path: str, check_magic_bytes_cb: Callable[[str], bool]):
    for root, _, filers in os.walk(path):
        is_empty = len(filers) == 0
        if is_empty: continue
        for file_path in filers:
            current_path = os.path.join(root, file_path)
            if not check_magic_bytes_cb(current_path):
                continue
            size_in_mb, created_at, modified_at = get_file_info(current_path)
            yield current_path, size_in_mb, created_at, modified_at
            

def add_export_strategies(name: str, strategy: ExportStrategy):
    global global_export_result_strategies
    assert isinstance(strategy, ExportStrategy), "invalid strategy instance"
    global_export_result_strategies[name.upper()] = strategy


def setup_and_run_scan_filers(path: str, file_strategy: str | None, export_result: str):
    file_strategy_resp = MAGIC_FILE_STRATEGIES.get(file_strategy)
    file_strategy_exists = file_strategy_resp is not None
    assert file_strategy_exists, f"file strategy not found {file_strategy}. You can try {','.join(MAGIC_FILE_STRATEGIES.keys())}"
    export_result_strategy_resp: ExportStrategy | None = global_export_result_strategies.get(export_result)
    export_result_strategy_exists = export_result_strategy_resp is not None
    assert export_result_strategy_exists, f"export result strategy not found {export_result}. You can try {','.join(global_export_result_strategies.keys())}"
    magic_bytes, read_size = file_strategy_resp
    check_magic_bytes_cb = factory_check_magic_bytes_from(magic_bytes, read_size)
    with export_result_strategy_resp() as strategy:
        for result in scan_filers(path, check_magic_bytes_cb):
            strategy.push_result(result)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Script to scan files, from magic bytes')
    parser.add_argument('path', metavar='PATH', type=str, nargs='?', default=os.getcwd(), help='Path to the directory to be scanned (default: current directory)')
    parser.add_argument('--file-strategy', metavar='FILE_STRATEGY', type=str, help='Strategy to scan the files: e.g.: SQLITE')
    parser.add_argument('--export-result', metavar='EXPORT_RESULT', type=str, default="CSV", help='Export result e.g.: SQLITE, CSV,  (default: CSV)')
    args = parser.parse_args()
    add_export_strategies("csv", ExportCSVStrategy)
    add_export_strategies("sqlite", ExportSQLITEStrategy)
    setup_and_run_scan_filers(args.path, args.file_strategy, args.export_result)