from pathlib import Path
import sys,subprocess
ROOT=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(ROOT/'src/paper2_foundation.py')],cwd=ROOT,check=True)
subprocess.run([sys.executable,str(ROOT/'src/make_release.py')],cwd=ROOT,check=True)
subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=ROOT,check=True)