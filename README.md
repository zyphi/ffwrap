# ffwrap

## ffwrap.py

Wrapper around FFmpeg with customized terminal output, metadata for input(s) and simple database.

### Dependencies

- python 3.10+
- ffmpeg
- mediainfo
- For Windows: colorama (`pip install colorama`)

### Usage

Use `python[3] path/to/ffwrap/ffwrap.py` (or just `ffwrap`, if there is an alias) instead of `ffmpeg` in your command line. Only differences:

- The output(s) must be preceded by `-o`.
- After the last output, the only valid options are `-y` and `-n`.

## ffquery.py

CLI tool for finding stuff in ffwrap's database.

### Usage

- h, --help --> show this help message and exit
- R --> reset database
- S --> show successful entries
- F --> show failed entries
- I --> show incomplete entries
- a --> show entries after date, excluded (YYYYMMDD). Special cases: "t" = today, "y" = yesterday, "n" = now.
- b --> show entries before date, included (YYYYMMDD). Special cases: "t" = today, "y" = yesterday, "n" = now.
- i --> find entries by input file (case insensitive)
- o --> find entries by output file (case insensitive)
- v --> print version number and exit

## Aliases

### Linux (Ubuntu 20.04, at least)

Save these two lines in .bashrc:

```bash
alias ffwrap='python3 /path/to/ffwrap/ffwrap.py'
alias ffquery='python3 /path/to/ffwrap/ffquery.py'
```

### Windows (10, at least)

Create these two .bat files in a folder that is in your PATH:

```bash
# ffwrap.bat
@echo off
python G:\DA-Tools\ffwrap\ffwrap.py %*
```

```bash
# ffquery.bat
@echo off
python G:\DA-Tools\ffwrap\ffquery.py %*
```
