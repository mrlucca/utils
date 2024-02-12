
---

# Scan scripts


---

## MAGIC-SCAN script
This script is used to scan files in a directory based on magic bytes and export the results to a specified format, such as CSV or SQLite.

### Usage

```bash
python magic-scan.py [path] [--file-strategy FILE_STRATEGY] [--export-result EXPORT_RESULT]
```

#### Arguments:

- `path` (optional): Path to the directory to be scanned. If not provided, the current directory will be used as default.

- `--file-strategy FILE_STRATEGY` (optional): Strategy for scanning the files. For example: `SQLITE`.

- `--export-result EXPORT_RESULT` (optional): Format for exporting the results. For example: `SQLITE`, `CSV`. The default is `CSV`.

### Usage Examples:

1. Scan the current directory using the default strategy (CSV) and export the results to a CSV file:

```bash
python magic-scan.py
```

2. Scan a specific directory using the `SQLITE` file strategy and export the results to a SQLite database:

```bash
python magic-scan.py /path/to/directory --file-strategy SQLITE --export-result SQLITE
```

3. Scan a specific directory using the default strategy (CSV) and export the results to a CSV file:

```bash
python magic-scan.py /path/to/directory
```

## Python Requirements:

This script requires Python 3.12 or higher. Make sure you have the appropriate version of Python installed before running the script.

---
