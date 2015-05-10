# -*- mode: python -*-

from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

a = Analysis(['..\\src\\main.py'],
             pathex=['C:\\Users\\juherask\\Projects\\inSVN\\KanjiQuest\\branches\\kivy_experiments\\build'],
             hiddenimports=[],
             #hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='KivyKanjiQuest.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='..\\assets\\kqico.ico')
coll = COLLECT(exe, #Tree('../src/',
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='KivyKanjiQuest')
