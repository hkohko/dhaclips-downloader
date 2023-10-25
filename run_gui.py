from pathlib import PurePath
from subprocess import run
from sys import platform

working_dir = PurePath(__file__).parents[0]
python = working_dir.joinpath(".venv", "Scripts", "python.exe")
if platform == "linux":
    python = working_dir.joinpath(".venv", "bin", "python3")
main_gui = working_dir.joinpath("src", "gui.py")
run([python, main_gui])