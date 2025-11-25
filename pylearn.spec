# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for PyLearn Desktop
# Run with: pyinstaller pylearn.spec

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Project root directory
project_root = os.path.dirname(os.path.abspath(SPEC))

# Collect PySide6 data files and submodules
pyside6_datas = collect_data_files('PySide6')
pyside6_submodules = collect_submodules('PySide6')

# Define data files to include
# Format: (source_path, destination_folder_in_bundle)
datas = [
    # Assets folder with styles, icons, and database
    (os.path.join(project_root, 'assets', 'styles'), os.path.join('assets', 'styles')),
    (os.path.join(project_root, 'assets', 'icons'), os.path.join('assets', 'icons')),
    (os.path.join(project_root, 'assets', 'pylearn.db'), 'assets'),
]

# Add PySide6 data files
datas.extend(pyside6_datas)

# Hidden imports for PySide6 and SQLite
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'sqlite3',
]
hiddenimports.extend(pyside6_submodules)

# Check if an icon file exists
icon_path = os.path.join(project_root, 'assets', 'icons', 'pylearn.ico')
if not os.path.exists(icon_path):
    icon_path = None

a = Analysis(
    [os.path.join(project_root, 'main.py')],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PyLearnDesktop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # --windowed mode (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,  # Application icon (if exists)
)
