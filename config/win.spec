# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['..\\nonmouse\\__main__.py'],
    pathex=[r'C:\Users\PAUL\OneDrive\Escritorio\LABORATORIOS Y PROYECTOS IV SEMESTRE\PF\IHCProyectoFinal\nonmouse'],  # Ruta de tu carpeta principal del paquete
    binaries=[],
    datas=[
        # Incluye los módulos necesarios de mediapipe y cv2 desde tu entorno virtual
        (r'c:\users\paul\onedrive\escritorio\laboratorios y proyectos iv semestre\pf\ihcproyectofinal\venv\lib\site-packages\mediapipe\modules', 'mediapipe\modules'),
        (r'c:\users\paul\onedrive\escritorio\laboratorios y proyectos iv semestre\pf\ihcproyectofinal\venv\lib\site-packages\cv2', 'cv2'),
    ],
    hiddenimports=['cv2', 'cv2.cv2', 'cv2.data', 'numpy', 'mediapipe'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NonMouse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # False = sin consola, True = con consola visible
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='..\\images\\icon.ico'  # Ícono del ejecutable
)