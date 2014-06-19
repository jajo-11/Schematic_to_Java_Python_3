import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], 'include_files': ['README.txt', 'logo.png']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Structure to Java Converter",
        version = "0.4",
        description = "Converts .schematics into java class so it can be used to spawn whatever was in the schematic as a dungeon.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Schematic_to_Java_Python_3.py", icon="logo.ico", base=base), Executable('MainWindow.py')])