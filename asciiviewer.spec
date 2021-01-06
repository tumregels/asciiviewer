# -*- mode: python ; coding: utf-8 -*-
import platform

block_cipher = None

if platform.system() == 'Windows':

    a = Analysis(['asciiviewer/AsciiViewer.py'],
                 pathex=['asciiviewer/source'],
                 binaries=[],
                 datas=[
                     ('asciiviewer/splash.jpg', '.'),
                     ('asciiviewer/default.cfg', '.'),
                     ('asciiviewer/example/fmap', 'example'),
                     ('asciiviewer/example/MCOMPO_UOX_TBH', 'example')
                 ],
                 hiddenimports=[],
                 hookspath=[],
                 runtime_hooks=[],
                 excludes=[],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 noarchive=True)
    pyz = PYZ(a.pure, a.zipped_data,
              cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              [],
              name='asciiviewer',
              debug=True,
              bootloader_ignore_signals=False,
              strip=False,
              upx=False,
              upx_exclude=[],
              runtime_tmpdir=None,
              console=False)

elif platform.system() == 'Linux':

    a = Analysis(['asciiviewer/AsciiViewer.py'],
                 pathex=['asciiviewer/source'],
                 binaries=[],
                 datas=[
                     ('asciiviewer/splash.jpg', '.'),
                     ('asciiviewer/default.cfg', '.'),
                     ('asciiviewer/example/fmap', 'example'),
                     ('asciiviewer/example/MCOMPO_UOX_TBH', 'example')
                 ],
                 hiddenimports=[],
                 hookspath=[],
                 runtime_hooks=[],
                 excludes=[],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 noarchive=False)
    pyz = PYZ(a.pure, a.zipped_data,
              cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              [],
              name='asciiviewer',
              debug=True,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              upx_exclude=[],
              runtime_tmpdir=None,
              console=True)

elif platform.system() == 'Darwin':

    a = Analysis(['asciiviewer/AsciiViewer.py'],
                 pathex=['asciiviewer/source'],
                 binaries=[],
                 datas=[
                     ('asciiviewer/splash.jpg', '.'),
                     ('asciiviewer/default.cfg', '.'),
                     ('asciiviewer/example/fmap', 'example'),
                     ('asciiviewer/example/MCOMPO_UOX_TBH', 'example')
                 ],
                 hiddenimports=['wx'],
                 hookspath=[],
                 runtime_hooks=[],
                 excludes=[],
                 win_no_prefer_redirects=False,
                 win_private_assemblies=False,
                 cipher=block_cipher,
                 noarchive=False)
    pyz = PYZ(a.pure, a.zipped_data,
              cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              [],
              name='asciiviewer',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              upx_exclude=[],
              runtime_tmpdir=None,
              console=False)
    app = BUNDLE(exe,
                 name='asciiviewer.app',
                 icon=None,
                 bundle_identifier=None)
