from pathlib import PurePath
from subprocess import run

working_dir = PurePath(__file__).parents[0]
python = working_dir.joinpath(".venv", "Scripts", "python.exe")
main_gui = working_dir.joinpath("src", "gui.py")
run([python, main_gui])
