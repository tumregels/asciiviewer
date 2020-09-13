# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['AsciiViewer.py'],
             pathex=['./source'],
             binaries=[],
             datas=[ ('splash.jpg', '.'), ('default.cfg', '.') ],
             hiddenimports=['wx'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += Tree('./example', prefix='example')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AsciiViewerMac',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='AsciiViewerMac.app',
             icon=None,
             bundle_identifier=None)
