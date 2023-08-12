# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['__init__.py', 'views\\CharacterPick.py', 'views\\Game.py', 'controllers\\Character.py', 'controllers\\Styler.py', 'Objects\\GameOverFrame.py', 'Objects\\Ground.py', 'Objects\\Heart.py', 'Objects\\Monster_Mushroom.py', 'Objects\\Player.py'],
             pathex=['C:\\Users\\x\\Desktop\\PyGame-1'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='Game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
