from pathlib import Path
import subprocess
import sys
import venv

root=Path(__file__).resolve().parent
python=root/'.venv/Scripts/python.exe'
if not python.exists():
    venv.EnvBuilder(with_pip=True).create(root/'.venv')
args=[str(python),'-m','pip','install','--disable-pip-version-check','-r',str(root/'tooling/requirements.lock.txt')]
if (root/'tooling/wheels').is_dir():
    args += ['--no-index','--find-links',str(root/'tooling/wheels')]
else:
    args += ['--timeout','120','--retries','5']
raise SystemExit(subprocess.run(args,cwd=root).returncode)
