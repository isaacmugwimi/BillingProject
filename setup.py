from cx_Freeze import setup, Executable, sys

includeFiles = ['icon2.ico']
exclude = []
packages = []
base = None
if sys.platform == 'win32':
    base = 'win32GUI'
shortcut_table = [
    (
        "DesktopShortcut",
        "DesktopFolder",
        "Billing System",
        "TARGETDIR",
        "[TARGETDIR]ProjectSplashScreen.exe",
        None,
        None,
        None,
        None,
        None,
        None,
        "TARGETDIR",
    )
]
msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {"data": msi_data}
setup(
    version="0.1",
    description="Billing System",
    author="Isaac Ireri",
    name="Billing System",
    options={'build_exe': {'include_files': includeFiles}, "bdist_msi": bdist_msi_options},
    executables=[
        Executable(
            script="ProjectSplashScreen.py",
            base=base,
            icon="icon2.ico"
        )
    ]
)
