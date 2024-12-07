# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['wxLife.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['wx.lib.pubsub'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
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
    name='wxLife',
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
    icon=['icon_512.icns'],
)
app = BUNDLE(
    exe,
    name='wxLife.app',
    icon='icon_512.icns',
    bundle_identifier=None,
)
