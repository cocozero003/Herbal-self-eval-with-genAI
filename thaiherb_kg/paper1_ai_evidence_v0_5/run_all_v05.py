"""Reproduce the candidate 19-class Paper 1 exploratory sensitivity analysis.

Does not claim recovery of original paper vectors or independent expert ratings.
"""
from pathlib import Path
import csv, json, sys, itertools
from statistics import mean
import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from formula_audit import verify
import model_reanalysis as model


def read_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    out = ROOT / 'results'
    input_path = ROOT / 'data' / 'paper1_bootstrap_v3_proxy.json'
    _, _, formula_audit = verify(input_path, out)
    assert formula_audit['present_memberships'] == 46
    assert formula_audit['positive_npmi_edges'] == 23
    chemistry = [a for a in json.loads(input_path.read_text(encoding='utf-8'))['assertions']
                 if a['assertion_type'] == 'ChemistryOccurrenceAssertion']
    taxonomy = {r['name']: r['class_v05'] for r in read_csv(out / 'CHEMICAL_IDENTITY_TAXONOMY_25.csv')}
    assert len(taxonomy) == 25 and len(set(taxonomy.values())) == 19
    assert set(taxonomy) == set(a['object_label'] for a in chemistry)
    model.CLASS.clear()
    model.CLASS.update(taxonomy)
    snapshot = json.loads((out / 'formula_reviewed_snapshot.json').read_text(encoding='utf-8'))
    model.train(snapshot, chemistry, out / '19_class_candidate')
    old = read_csv(out / 'BASELINE_v04_18class_cosines.csv')
    new = read_csv(out / '19_class_candidate' / 'embedding_cosine_45pairs_10seeds.csv')
    records = []
    for m in ('Chem-Proxy', 'Core-Proxy'):
        for seed in model.SEEDS:
            aa = {(r['herb_a'], r['herb_b']): float(r['cosine']) for r in old
                  if r['model'] == m and int(r['seed']) == seed}
            bb = {(r['herb_a'], r['herb_b']): float(r['cosine']) for r in new
                  if r['model'] == m and int(r['seed']) == seed}
            assert len(aa) == len(bb) == 45
            kk = list(aa)
            v1 = np.asarray([aa[k] for k in kk]); v2 = np.asarray([bb[k] for k in kk])
            s1 = set(sorted(kk, key=lambda k: aa[k], reverse=True)[:5])
            s2 = set(sorted(kk, key=lambda k: bb[k], reverse=True)[:5])
            records.append({'model': m, 'seed': seed,
              'rank_rho_v04_18_vs_v05_19': round(float(spearmanr(v1, v2).statistic), 7),
              'mean_abs_cosine_delta': round(float(np.abs(v1 - v2).mean()), 7),
              'top5_overlap': len(s1 & s2), 'v04_class_count': 18,
              'candidate_v05_class_count': 19,
              'comparison_kind': 'class_annotation_perturbation_NOT_original_manuscript_replication'})
    write_csv(out / 'CLASS_TAXONOMY_ABLATION_10SEEDS.csv', records)
    summary = json.loads((out / 'CURATION_AND_ABLATION_SUMMARY.json').read_text(encoding='utf-8'))
    for m in ('Chem-Proxy', 'Core-Proxy'):
        mr = [r for r in records if r['model'] == m]
        assert abs(summary[m]['mean_rho'] - mean(r['rank_rho_v04_18_vs_v05_19'] for r in mr)) < 1e-6
    print(json.dumps({'audit': formula_audit['dataset_projection_matches_source_tables'],
                      'ablation_rows': len(records),
                      'chem_mean_rho': summary['Chem-Proxy']['mean_rho'],
                      'core_mean_rho': summary['Core-Proxy']['mean_rho'],
                      'scientific_status': 'AI-assisted exploratory; original Paper 1 class mapping not recovered'},
                      ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()