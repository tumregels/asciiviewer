# -*- mode: python -*-
a = Analysis(['asciiviewer/AsciiViewer.py'],
             pathex=['./asciiviewer', './asciiviewer/source'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('splash.jpg', './asciiviewer/splash.jpg', 'DATA'),
            ('default.cfg', './asciiviewer/default.cfg', 'DATA')]
a.datas += Tree('./asciiviewer/example', prefix='example')
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='asciiviewer',
          debug=True,
          strip=None,
          upx=True,
          console=True)
