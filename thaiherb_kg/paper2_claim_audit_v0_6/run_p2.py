from src.build import build_p2, make_dashboard
if __name__=='__main__':
    build_p2()
    make_dashboard('Paper 2 v0.6 | Compound-Level Source Review','P2_CHEM_EVIDENCE_100_v06.csv','Paper2_ClaimAudit_v0.6.html',
        '100 original research assertions; five analytically source-matched from Piper retrofractum; 95 remain unverified. No expert gold labels.')
    print('Paper 2 v0.6 audit artifacts rebuilt')
