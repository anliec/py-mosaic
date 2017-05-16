# -*- mode: python -*-

block_cipher = None


a = Analysis(['mosaic.py'],
             pathex=['/home/nicolas/Documents/Programation/Python/Photos'],
             binaries=[('mosaic_fr.qm', '.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mosaic',
          debug=False,
          strip=False,
          upx=True,
          console=True )
