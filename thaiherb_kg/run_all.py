"""Execute the paper-specific data audits in order."""
import json
from audit import run as audit
from paper1.run import run as p1
from paper2.run import run as p2
from paper3.run import run as p3
if __name__=='__main__':
    print('DATA AUDIT',json.dumps(audit()['crosswalk']))
    print('PAPER 1',json.dumps(p1()))
    print('PAPER 2',json.dumps(p2()))
    print('PAPER 3',json.dumps(p3()))
