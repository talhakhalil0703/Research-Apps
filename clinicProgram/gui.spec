# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['gui.py'],
             pathex=['C:\\Users\\Talha Khalil\\Desktop\\clinicProgram'],
             binaries=[],
             datas=[],
             hiddenimports=['openpyxl','pyexcel_io.readers.csvr', 'pyexcel_io.readers.csvz', 'pyexcel_io.readers.tsv', 'pyexcel_io.readers.tsvz', 'pyexcel_io.writers.csvw', 'pyexcel_io.readers.csvz', 'pyexcel_io.readers.tsv', 'pyexcel_io.readers.tsvz', 'pyexcel_io.database.importers.django', 'pyexcel_io.database.importers.sqlalchemy', 'pyexcel_io.database.exporters.django', 'pyexcel_io.database.exporters.sqlalchemy', 'pyexcel_xlsx', 'pyexcel_xlsx.xlsxr', 'pyexcel_xlsx.xlsxw', 'pyexcel_xlsxw', 'pyexcel_xlsxw.xlsxw', 'pyexcel_xls', 'pyexcel_xls.xlsr', 'pyexcel_xls.xlsw', 'pyexcel.plugins', 'pyexcel.plugins.parsers', 'pyexcel.plugins.renderers', 'pyexcel.plugins.sources', 'pyexcel.plugins.sources.file_input', 'pyexcel.plugins.parsers.excel', 'pyexcel.plugins.sources.pydata', 'pyexcel.plugins.sources.pydata.arraysource', 'pyexcel.plugins.sources.file_output', 'pyexcel.plugins.renderers.excel', 'pyexcel-xlsx', 'pyexcel-xlsxw'],
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
          name='gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
