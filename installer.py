from cx_Freeze import setup, Executable
import sys
import os

file = os.path.dirname(os.path.abspath(sys.argv[0]))
exe = Executable(
    script=os.path.join(file, "FileChecker", "FileChecker.py"),
    icon=os.path.join(file, "FileChecker", "FileCheckerIcon.ico")
)

setup(
    executables=[exe]
)