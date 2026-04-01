# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile

#
# Project settings
#
EE_EXPORT_EXEC_NAME = os.environ.get("EE_EXPORT_EXEC_NAME", os.getcwd())
EE_EXPORT_DEBUG_MODE = os.environ.get("EE_EXPORT_DEBUG_MODE", os.getcwd()) == "1"

print("Project name:", EE_EXPORT_EXEC_NAME)
print("Project debug:", EE_EXPORT_DEBUG_MODE)

#
# Get the core dir, development is root of git project
# when frozen/packaged its MEIPASS folder
#
EE_CORE = os.environ.get("EE_CORE_DIR", os.getcwd())
print("Detected core path:", EE_CORE)

# ------------------------------------------------------
# Copy dependency files and folders
# ------------------------------------------------------
files_to_copy = {
    os.path.join(EE_CORE, "engine/main.py"):       "temp/main.py",
}

folders_to_copy = {
    os.path.join(EE_CORE, "engine/modules"):       "temp/modules",
    os.path.join(EE_CORE, "engine/gameObjects"):   "temp/gameObjects",
    os.path.join(EE_CORE, "engine/assimp"):        "temp/assimp",
    "assets":                                       "export/assets",
    "engine/shaders":                              "export/shaders",
    "engine/engineAssets":                         "export/engineAssets",
}

for src, dst in folders_to_copy.items():
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

for src, dst in files_to_copy.items():
    if os.path.isfile(src):
        shutil.copy2(src, dst)

# ------------------------------------------------------
# Configuration
# ------------------------------------------------------
a = Analysis(
    ['temp/main.py'],
    pathex=[],
    binaries=[('temp/assimp/assimp.dll', 'pygame.')],
    datas=[],
    hiddenimports=['gameObjects.scriptBehaivior'],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=['engine/hooks/hook_ee_export.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=EE_EXPORT_EXEC_NAME,
    debug=EE_EXPORT_DEBUG_MODE,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=EE_EXPORT_DEBUG_MODE,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='engine/engineAssets/icon/icon.ico',
)
