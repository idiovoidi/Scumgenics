# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Scumgenics Save Manager.

Build instructions:
    pyinstaller Scumgenics.spec

Output:
    dist/Scumgenics.exe - Standalone executable
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Collect all PyQt6 submodules to ensure GUI works properly
pyqt6_hiddenimports = collect_submodules('PyQt6')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include README for users
        ('README.md', '.'),
    ],
    hiddenimports=[
        # Explicitly include all src modules
        'src.save_manager',
        'src.main_window',
        'src.logging_config',
        'src.backup_info',
        'src.file_operations',
        'src.path_builder',
        'src.result',
        'src.save_manager_config',
        'src.settings',
        'src.options_dialog',
        # PyQt6 modules
        *pyqt6_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude test dependencies to reduce size
        'pytest',
        'pytest-qt',
        'pytest-mock',
        'hypothesis',
        'coverage',
        '_pytest',
        'py.test',
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
    name='Scumgenics',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you create one: icon='icon.ico'
)
