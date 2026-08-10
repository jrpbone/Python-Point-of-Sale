# Building PyPOS for Windows

PyPOS is packaged as a standalone 64-bit Windows executable with PyInstaller.
The resulting file can run without a separate Python installation.

## Prerequisites

- 64-bit Windows
- Python 3.12 or later, including a working Tcl/Tk installation
- `pip`

Confirm that Python and Tkinter are available:

```powershell
python --version
python -c "import tkinter; tkinter.Tcl(); print('Tkinter is available')"
```

## Install build dependencies

From the repository root, install the application dependencies and PyInstaller:

```powershell
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

Using a clean virtual environment is recommended for repeatable release builds:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

## Run the tests

Run the test suite before creating a release build:

```powershell
python test.py
```

## Build the standalone executable

Run PyInstaller with the committed specification file:

```powershell
python -m PyInstaller --noconfirm --clean PyPOS.spec
```

The standalone executable is created at:

```text
dist\PyPOS.exe
```

The specification file configures the application as a one-file, windowed
executable and bundles the icon, application assets, sample product workbook,
OpenPyXL, and the required Tcl/Tk resources.

## Verify the build

Launch the executable and confirm that the login window appears:

```powershell
.\dist\PyPOS.exe
```

Generate a SHA-256 checksum for the release notes:

```powershell
Get-FileHash .\dist\PyPOS.exe -Algorithm SHA256
```

Runtime databases, logs, backups, and generated spreadsheets are stored under:

```text
%LOCALAPPDATA%\PyPOS
```

They are not embedded into the executable or written into PyInstaller's
temporary extraction directory.

## Publish a GitHub release

Upload `dist\PyPOS.exe` as the release asset. Include its SHA-256 checksum in
the release notes so users can verify the download.

Do not upload the `build\` directory. The `dist\` and `build\` directories are
generated locally and should remain excluded from Git; commit `PyPOS.spec` and
this build guide instead.

## Troubleshooting

### Tkinter or `init.tcl` is unavailable

If the Tkinter prerequisite check fails, repair or reinstall Python with the
Tcl/Tk and IDLE component enabled. Do not publish an executable from a build
that reports that Tkinter was excluded.

### Windows SmartScreen warning

Unsigned executables can trigger a Windows SmartScreen warning after download.
For public production releases, sign `PyPOS.exe` with a trusted code-signing
certificate before uploading it.
