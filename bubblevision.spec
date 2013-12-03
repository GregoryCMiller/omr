# -*- mode: python -*-
a = Analysis(['omr\\omrcmd.py'],
             pathex=['F:\\Dropbox\\Git\\omr'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='bubblevision.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
