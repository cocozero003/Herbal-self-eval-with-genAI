"""Rebuild the v0.6 source qualification, coverage gates, and exploratory models."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for filename in ('evidence_qualification.py','source_holdout_embedding.py','generate_dashboard.py'):
 subprocess.run([sys.executable,str(ROOT/'audit_v06'/filename)],cwd=ROOT,check=True)
subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=ROOT,check=True)