# -*- mode: python ; coding: utf-8 -*-
import platform

block_cipher = None

datas = [
    ('asciiviewer/assets/splash.png', 'assets'),
    ('asciiviewer/assets/default.cfg', 'assets'),
    ('asciiviewer/examples/fmap', 'examples'),
    ('asciiviewer/examples/MCOMPO_UOX_TBH', 'examples')
]

if platform.system() == 'Windows':

    a = Analysis(['asciiviewer/main.py'],
                 pathex=[],
                 binaries=[],
                 datas=datas,
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
              console=False,
              icon='asciiviewer/assets/icon.ico')

elif platform.system() == 'Linux':

    a = Analysis(['asciiviewer/main.py'],
                 pathex=[],
                 binaries=[],
                 datas=datas,
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

    a = Analysis(['asciiviewer/main.py'],
                 pathex=[],
                 binaries=[],
                 datas=datas,
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
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              upx_exclude=[],
              runtime_tmpdir=None,
              console=False,
              icon='asciiviewer/assets/icon.icns')
    app = BUNDLE(exe,
                 name='asciiviewer.app',
                 icon='asciiviewer/assets/icon.icns',
                 bundle_identifier=None)
