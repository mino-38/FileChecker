from cx_Freeze import setup, Executable
import os
import sys

_root = os.path.dirname(os.path.abspath(sys.argv[0]))
base = "Win32GUI" if sys.platform == "win32" else None
exe = Executable(script=os.path.join(_root, "FileChecker", "FileChecker.py"), base=base, icon=os.path.join(_root, "FileCheckerIcon.ico"))

setup(
    executables=[exe]
)