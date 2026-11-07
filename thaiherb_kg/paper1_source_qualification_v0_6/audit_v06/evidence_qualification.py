"""Paper 1 v0.6: strict, explicitly non-independent literature corroboration and source-dependence audit.

No automated scraping, no fabricated experts, no original training archive claims.
Only manually catalogued publicly retrievable studies are recorded as candidate corroboration.
"""
from __future__ import annotations
import csv, json, hashlib
from pathlib import Path
from collections import Counter, defaultdict
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'results'
OUT = R / 'v06'

# URL: public evidence locator / focus material / method / scope
# These candidate corroborations were inspected from public source summaries/abstracts on 2026-11-07.
SOURCES = {
 'GINGER_HPLC_2007': ('https://pubmed.ncbi.nlm.nih.gov/17955965/', 'primary_analytical', 'Zingiber officinale raw ginger and dried aqueous extract', 'HPLC and ESI-MS/MS', '6-gingerol; 6-shogaol', 'exact_species_raw_plant_or_extract'),
 'PIPER_LCMS_2021': ('https://pmc.ncbi.nlm.nih.gov/articles/PMC8533580/', 'primary_analytical', 'Piper retrofractum fruit extract', 'LC-HRMS/MS profiling', 'piperine; piperlongumine', 'exact_species_reported_plant_material'),
 'PEPPER_GCMS_2019': ('https://pmc.ncbi.nlm.nih.gov/articles/PMC6930617/', 'primary_analytical', 'Piper nigrum fruit oil', 'GC-MS', 'beta-caryophyllene; limonene', 'exact_species_essential_oil'),
 'GARLIC_GCMS_2017': ('https://pmc.ncbi.nlm.nih.gov/articles/PMC5575638/', 'primary_analytical', 'Allium sativum essential oil, hydrodistilled', 'GC-MS', 'diallyl sulfide', 'processed_distillate_only'),
 'PHLAI_DMSC': ('https://bdn-thp.dmsc.moph.go.th/ebook/qQycZ3tmpR9gC3q0GT5gMJq0qT5co3uw', 'government_monograph', 'Zingiber montanum hydrodistillate', 'quality marker monograph', 'sabinene; terpinen-4-ol', 'exact_species_extract'),
 'GALANGAL_1985': ('https://pubmed.ncbi.nlm.nih.gov/17345272/', 'primary_isolation', 'Alpinia galanga dried rhizomes', 'MS and NMR', "1'-acetoxychavicol acetate; 1'-acetoxyeugenol acetate", 'exact_species_rhizome'),
 'BASIL_SPECIES_REVIEW_2023': ('https://pmc.ncbi.nlm.nih.gov/articles/PMC10061529/', 'systematic_review', 'Ocimum tenuiflorum various accessions', 'systematic literature review', 'rosmarinic acid; oleanolic acid', 'species_level_not_red_cultivar'),
 'BASIL_RED_PRIMARY_2022': ('https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2022.1008917/full', 'primary_analytical', 'Ocimum tenuiflorum R cultivar, leaves', 'GC profiling', 'eugenol', 'red_cultivar_specific'),
 'LICORICE_HPLC_2007': ('https://www.sciencedirect.com/science/article/pii/S1570023206010270', 'primary_analytical', 'Glycyrrhizae Radix multi-sample material', 'HPLC', 'glycyrrhizin; liquiritin; liquiritigenin', 'genus_or_material_not_species_authenticated'),
 'CLOVE_GENOME_2022': ('https://www.nature.com/articles/s42003-022-03618-z', 'primary_analytical', 'Syzygium aromaticum leaves and buds', 'UHPLC and GC-MS', 'eugenol; eugenyl acetate; beta-caryophyllene', 'exact_species_bud_and_leaf'),
 'KAFFIR_GCMS_2021': ('https://pubmed.ncbi.nlm.nih.gov/33597415/', 'primary_analytical', 'Citrus hystrix peel essential oil', 'GC-MS', 'beta-pinene; D-limonene; sabinene', 'exact_species_peel_oil'),
 'KAFFIR_GCMS_2023': ('https://pubmed.ncbi.nlm.nih.gov/36985567/', 'primary_analytical', 'Citrus hystrix peel oil', 'GC-MS', 'sabinene; beta-pinene; limonene', 'exact_species_peel_oil'),
}

# Links are candidate corroboration for each specific herb-compound statement, not new unbiased training labels.
CORROBORATIONS = {
 'CA001': ['GINGER_HPLC_2007'], 'CA002':['GINGER_HPLC_2007'],
 'CA006':['PIPER_LCMS_2021'], 'CA008':['PIPER_LCMS_2021'],
 'CA012':['PEPPER_GCMS_2019'], 'CA013':['PEPPER_GCMS_2019'],
 'CA018':['GARLIC_GCMS_2017'],
 'CA021':['PHLAI_DMSC'], 'CA023':['PHLAI_DMSC'],
 'CA026':['GALANGAL_1985'],'CA027':['GALANGAL_1985'],
 'CA031':['BASIL_SPECIES_REVIEW_2023'],'CA032':['BASIL_SPECIES_REVIEW_2023'],
 'CA035':['BASIL_RED_PRIMARY_2022'],
 'CA036':['LICORICE_HPLC_2007'],'CA037':['LICORICE_HPLC_2007'],'CA038':['LICORICE_HPLC_2007'],
 'CA041':['CLOVE_GENOME_2022'],'CA042':['CLOVE_GENOME_2022'],'CA043':['CLOVE_GENOME_2022'],
 'CA046':['KAFFIR_GCMS_2021','KAFFIR_GCMS_2023'],
 'CA047':['KAFFIR_GCMS_2021','KAFFIR_GCMS_2023'],
 'CA048':['KAFFIR_GCMS_2021','KAFFIR_GCMS_2023']
}

CONTEXT_WARNINGS = {
 'CA003':'Only review-level source is retained. Direct primary specimen confirmation of zingerone not supplied.',
 'CA018':'Detected in garlic distilled essential oil. This is not direct presence in unprocessed cloves; heat/distillation creates transformation products.',
 'CA022':'DMPBD has a literature expansion but no unambiguous PubChem CID in the locked identity table.',
 'CA031':'Species-level evidence; red-cultivar-specific assay is not established.',
 'CA032':'Species-level evidence; red-cultivar-specific assay is not established.',
 'CA035':'R-cultivar GC profile is context-specific; concentrations cannot be generalized across accession or extraction.',
 'CA036':'HPLC in mixed Glycyrrhizae Radix samples is not species-authenticated G. glabra evidence.',
 'CA037':'HPLC in mixed Glycyrrhizae Radix samples is not species-authenticated G. glabra evidence.',
 'CA038':'HPLC in mixed Glycyrrhizae Radix samples is not species-authenticated G. glabra evidence.',
 'CA047':'Original generic limonene occurrence is not stereochemically resolved; D-limonene study must not be used to force PubChem isomer ID.',
 'CA008':'Distinguish piperlongumine from piperlonguminine, different chemical structures.',
}

def read_csv(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def save_csv(p,rows):
    if not rows:raise ValueError('empty dataset')
    p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def sha256(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def audit():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=read_csv(R/'CHEMICAL_ASSERTION_EVIDENCE_REVIEW_30.csv')
    classes=read_csv(R/'CHEMICAL_IDENTITY_TAXONOMY_25.csv')
    assert len(rows)==30 and len(classes)==25
    ids={x['assertion_id'] for x in rows}
    assert set(CORROBORATIONS)<=ids
    base_by_herb=defaultdict(set)
    for x in rows:base_by_herb[x['herb_id']].add(x['occurrence_source_id'])
    assessed=[]; reviewed_sources=[]
    for key,(url,kind,material,method,chemical,scope) in SOURCES.items():
        reviewed_sources.append({'source_key':key,'source_url':url,'source_type':kind,'study_material':material,
                                 'analytical_method_or_design':method,'compounds_stated':chemical,'source_scope':scope,
                                 'review_basis':'AI-assisted public-page abstract/content summary; no full-text line audit',
                                 'verification_date':'2026-11-07','is_new_training_source':0})
    for row in rows:
        aid=row['assertion_id']; links=CORROBORATIONS.get(aid,[])
        primary=[x for x in links if SOURCES[x][1].startswith('primary')]
        govt=[x for x in links if SOURCES[x][1]=='government_monograph']
        restricted=[x for x in links if SOURCES[x][5] in ('species_level_not_red_cultivar','genus_or_material_not_species_authenticated','processed_distillate_only')]
        # A source being a primary paper never proves strain/part/processing match unless explicitly stated.
        if primary and not restricted:grade='PRIMARY_CANDIDATE_CONTEXTUAL'
        elif primary and restricted:grade='PRIMARY_WITH_CONTEXT_LIMITATION'
        elif govt:grade='GOVERNMENT_MONOGRAPH_CORROBORATED'
        elif links:grade='SECONDARY_ONLY_CORROBORATION'
        elif row['source_type'].startswith('primary'):grade='PRIMARY_SOURCE_IN_V05_ONLY'
        elif row['source_type']=='government_monograph':grade='GOVERNMENT_SOURCE_IN_V05_ONLY'
        else:grade='SECONDARY_ONLY_V05_OR_UNRESOLVED'
        assessed.append({
            'assertion_id':aid,'herb_id':row['herb_id'],'botanical_name':row['herb_scientific'],
            'compound':row['compound_source_name'],'original_v05_source_id':row['occurrence_source_id'],
            'original_v05_source_type':row['source_type'],'original_source_url':row['occurrence_source_url'],
            'additional_source_keys':';'.join(links),'additional_source_urls':';'.join(SOURCES[x][0] for x in links),
            'independent_additional_paper_count':len({SOURCES[x][0] for x in links}),
            'new_primary_corroboration_count':len(primary),'new_government_corroboration_count':len(govt),
            'qualification_status':grade,'context_limitation':CONTEXT_WARNINGS.get(aid,''),
            'identity_warning':('CID missing / stereoisomer unresolved' if not row['pubchem_cid_candidate'] else ''),
            'original_paper1_compound_class_recovered':0,'independent_expert_validated':0,
            'research_note':'Literature corroboration is a post-hoc source review; not independent model validation.'
        })
    save_csv(OUT/'assertion_evidence_qualification_30.csv',assessed)
    save_csv(OUT/'new_public_study_registry_12.csv',reviewed_sources)
    nsrc=Counter(x['occurrence_source_id'] for x in rows)
    network=[]
    for herb in sorted(base_by_herb):
        group=[x for x in rows if x['herb_id']==herb]
        source=base_by_herb[herb]
        extras={url for x in group for key in CORROBORATIONS.get(x['assertion_id'],[]) for url in [SOURCES[key][0]]}
        network.append({'herb_id':herb,'original_assertions':len(group),'original_distinct_sources':len(source),
                        'original_top_source_share':max(nsrc[s] for s in source if s in nsrc)/len(group) if len(source)==1 else max(sum(z['occurrence_source_id']==s for z in group) for s in source)/len(group),
                        'added_candidate_study_urls':len(extras),'has_primary_additional_evidence':int(any(SOURCES[key][1].startswith('primary') for x in group for key in CORROBORATIONS.get(x['assertion_id'],[]))),
                        'original_single_source_fragility':int(len(source)==1),
                        'note':'Secondary references may describe same underlying experiments; independent evidence not guaranteed.'})
    save_csv(OUT/'herb_source_independence_10.csv',network)
    # Remove one SOURCE from original locked v0.5 ledger; count total isolated/unsupported herb rows.
    holdout=[]
    for source in sorted(set(x['occurrence_source_id'] for x in rows)):
        survivors=[x for x in rows if x['occurrence_source_id']!=source]
        valid={x['herb_id'] for x in survivors}
        lost={x['herb_id'] for x in rows}-{x['herb_id'] for x in survivors}
        holdout.append({'removed_source_id':source,'source_assertions_removed':sum(x['occurrence_source_id']==source for x in rows),
                        'retained_assertions':len(survivors),'herbs_without_any_chemistry':len(lost),
                        'unrepresented_herbs':';'.join(sorted(lost)),
                        'interpretation':'Source-coverage stress test (not trained embedding or biological performance)'})
    save_csv(OUT/'leave_one_source_out_12.csv',holdout)
    # Unlabeled independent dyads remain unfilled; template expected from prior v0.5
    gold=read_csv(R/'INDEPENDENT_DYAD_EXPERT_BLIND_45.csv')
    assert len(gold)==45 and all(not r['expert1_label'] and not r['adjudicated_label'] for r in gold)
    counts=Counter(x['qualification_status'] for x in assessed)
    result={'version':'v0.6','date':'2026-11-07','stage':'AI_LITERATURE_CORROBORATION_NOT_PRIMARY_FULLTEXT_ADJUDICATION',
            'locked_proxy_assertions':len(rows),'unique_compound_names':len(classes),'original_source_ids':len(nsrc),
            'original_herbs_with_single_source':sum(len(v)==1 for v in base_by_herb.values()),
            'new_potential_corroborating_papers_or_monographs':len(SOURCES),
            'corroborated_assertions_count':sum(bool(CORROBORATIONS.get(r['assertion_id'])) for r in rows),
            'qualification_count_by_status':dict(counts),
            'holdout_runs':len(holdout),
            'max_herbs_disconnected_after_single_source_removal':max(r['herbs_without_any_chemistry'] for r in holdout),
            'red_cultivar_and_part_issues':'H07 CA031/CA032 species-level support is not red-cultivar confirmation; H04 CA018 distilled oil, not fresh clove.',
            'compound_class_matches_original_paper1':False,
            'independent_expert_evaluation':False,
            'primary_fulltext_quote_audit_complete':False,
            'full_archive_identity_recovered':False,
            'frozen_dataset_hash_sha256':sha256(ROOT/'data/paper1_bootstrap_v3_proxy.json'),
            'guardrail':'DO NOT use numerical source counts as efficacy scores or gold standard labels.'}
    (OUT/'evidence_qualification_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))