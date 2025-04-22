# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../kmeans_gui.py'],
    pathex=['/home/kevin/machine_learning/src'],  # Agrega la ruta base del proyecto
    binaries=[],
    datas=[
        ('../../../icons/kmeans_icon.ico', '.'),
        ('../../../../datos_prueba.csv', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
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
    name='kmeans_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../../../icons/kmeans_icon.ico',
)
