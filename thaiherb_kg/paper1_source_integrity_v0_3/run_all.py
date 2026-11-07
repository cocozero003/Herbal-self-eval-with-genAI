"""Repeat the bounded source integrity analysis and the Cooc sensitivity test."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for script in ('audit_paper1.py','embedding_sensitivity.py'):
    subprocess.run([sys.executable,str(root/'src'/script),'--data',str(root/'data/paper1_bootstrap_v3_proxy.json'),'--out',str(root/'results')],check=True)
subprocess.run([sys.executable,'-m','pytest','-q',str(root/'tests')],check=True)