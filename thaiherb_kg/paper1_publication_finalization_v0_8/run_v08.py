from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(ROOT/'src/final_reanalysis.py')],cwd=ROOT,check=True)
subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=ROOT,check=True)