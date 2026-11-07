from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(ROOT/'src/reanalyse.py')],check=True,cwd=ROOT)
subprocess.run([sys.executable,'-m','pytest','-q','tests'],check=True,cwd=ROOT)