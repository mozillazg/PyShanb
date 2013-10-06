# -*- mode: python -*-
a = Analysis(['shanbay.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='shanbay.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True,
          icon='shanbay.ico'
          )
