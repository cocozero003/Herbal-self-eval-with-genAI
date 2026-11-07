from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for name in ['validate_heldout_formulas.py','prepare_expert_review.py','evaluate_expert_labels.py','create_dashboard.py']:
 subprocess.run([sys.executable,str(root/'src'/name)],cwd=root,check=True)
subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=root,check=True)