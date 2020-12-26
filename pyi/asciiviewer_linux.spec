# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['./asciiviewer/AsciiViewer.py'],
             pathex=['.', './asciiviewer/source'],
             binaries=[],
             datas=[('./asciiviewer/splash.jpg', '.'), ('./asciiviewer/default.cfg', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += Tree('./asciiviewer/example', prefix='example')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AsciiViewer',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
