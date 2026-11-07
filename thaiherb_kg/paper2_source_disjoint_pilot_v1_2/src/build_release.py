"""Build source-traceable claim audit, post-hoc external evidence panel and review forms.

No expert labels, primary citation confirmations, or original 35-class identifiers
are imputed from the chemical names or later literature.
"""
from __future__ import annotations
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
DATE = '2026-11-07'

def readcsv(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def writecsv(path, records, fields=None):
    records = list(records)
    fields = fields or list(records[0])
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fields, extrasaction='ignore'); w.writeheader(); w.writerows(records)

claims = readcsv(DATA / 'P2_ORIGINAL_SOURCE_TRACE_100_v11.csv')
assert len(claims) == 100 and len({x['assertion_id'] for x in claims}) == 100
by_material = {(x['herb_id'],x['compound_locked'].lower()):x for x in claims}

# These are exact reported analyte proportions from listed tables. Positive-only;
# neither non-detected controls nor clinical effects are inferred.
sources = [
    dict(source_id='EXT_CITRUS_LONG_2023',doi='10.11002/kjfp.2023.30.3.395',
         url='https://www.ekosfop.or.kr/archive/view_article_pubreader?pid=kjfp-30-3-395',
         citation='Long, D. M., Quoc, L. P. T., Nhung, T. T. P., Thy, V. B., & Nhu, N. L. Q. (2023). Chemical profiles and biological activities of essential oil of Citrus hystrix DC. peels. Korean Journal of Food Preservation, 30(3), 395–404. https://doi.org/10.11002/kjfp.2023.30.3.395',
         study_class='PRIMARY_ANALYTICAL_GC_MS',source_disjoint='YES_DOI',
         prior_development_overlap='NOT_FOUND_IN_FROZEN_SOURCE_IDS',part='fruit peel',
         preparation='steam-distilled peel essential oil',assay='GC-MS',locator='Table 2',
         primary_eligible='YES_POSITIVE_ONLY_POSTHOC'),
    dict(source_id='EXT_CLOVE_MOL2026',doi='10.3390/molecules31183292',
         url='https://www.mdpi.com/1420-3049/31/18/3292',
         citation='Sytykiewicz, H., Łukasik, I., & Goławska, S. (2026). GC-MS profiling, antioxidant and enzyme inhibitory activities of basil (Ocimum basilicum L.) and clove (Syzygium aromaticum L.) essential oils and their binary mixtures. Molecules, 31(18), 3292. https://doi.org/10.3390/molecules31183292',
         study_class='PRIMARY_ANALYTICAL_GC_MS',source_disjoint='YES_DOI',
         prior_development_overlap='NOT_FOUND_IN_FROZEN_SOURCE_IDS',part='commercial essential oil; exact plant part not confirmed',
         preparation='clove essential oil',assay='GC-MS',locator='Table 2',
         primary_eligible='CONDITIONAL_MATERIAL_CONTEXT'),
    dict(source_id='EXT_CURCUMA_LEAF_2022',doi='10.3390/antibiotics11111547',
         url='https://pmc.ncbi.nlm.nih.gov/articles/PMC9686912/',
         citation='Albaqami, J. J., et al. (2022). Chemical composition and biological activities of the leaf essential oils of Curcuma longa, Curcuma aromatica and Curcuma angustifolia. Antibiotics, 11(11), 1547. https://doi.org/10.3390/antibiotics11111547 (Full author list to verify before APA 7 submission).',
         study_class='PRIMARY_ANALYTICAL_GC_MS',source_disjoint='YES_ARTICLE',
         prior_development_overlap='NOT_FOUND_IN_FROZEN_SOURCE_IDS',part='leaves',
         preparation='leaf essential oil',assay='GC-MS',locator='Table 2, C. aromatica rows',
         primary_eligible='YES_POSITIVE_ONLY_POSTHOC'),
    dict(source_id='EXT_CORIANDER_SATYAL2020',doi='10.1177/1934578X20933067',
         url='https://journals.sagepub.com/doi/10.1177/1934578X20933067',
         citation='Satyal, P., & Setzer, W. N. (2020). Chemical compositions of commercial essential oils from Coriandrum sativum fruits and aerial parts. Natural Product Communications. https://doi.org/10.1177/1934578X20933067',
         study_class='PRIMARY_ANALYTICAL_GC_MS',source_disjoint='YES_DOI',
         prior_development_overlap='YES_USED_FOR_V10_CORROBORATION',part='commercial coriander fruit oils',
         preparation='commercial essential oil',assay='GC-MS',locator='Table 3',
         primary_eligible='EXCLUDE_LEAKAGE'),
]
writecsv(OUT/'P2_EXTERNAL_SOURCE_REGISTRY_V12.csv',sources)

panel_specs = [
    ('EXT_CITRUS_LONG_2023','H10','beta-pinene',30.19),
    ('EXT_CITRUS_LONG_2023','H10','limonene',22.15),
    ('EXT_CITRUS_LONG_2023','H10','sabinene',21.37),
    ('EXT_CITRUS_LONG_2023','H10','citronellal',6.17),
    ('EXT_CITRUS_LONG_2023','H10','terpinen-4-ol',4.88),
    ('EXT_CLOVE_MOL2026','H09','eugenol',55.0),
    ('EXT_CLOVE_MOL2026','H09','eugenyl acetate',4.7),
    ('EXT_CLOVE_MOL2026','H09','beta-caryophyllene',32.9),
    ('EXT_CLOVE_MOL2026','H09','alpha-humulene',3.5),
    ('EXT_CLOVE_MOL2026','H09','methyl salicylate',0.1),
    ('EXT_CURCUMA_LEAF_2022','H20','curdione',15.31),
]
source_lookup = {s['source_id']:s for s in sources}
panel=[]
for i,(source_id,herb,compound,reported_pct) in enumerate(panel_specs,1):
    assert (herb,compound) in by_material,(herb,compound)
    s=source_lookup[source_id]
    r=by_material[(herb,compound)]
    panel.append(dict(case_id=f'EXTC{i:03}',assertion_id=r['assertion_id'],herb_id=herb,
                      scientific_name=r['scientific_name_locked'],compound=compound,
                      source_id=source_id,doi=s['doi'],source_url=s['url'],
                      plant_part=s['part'],preparation=s['preparation'],assay=s['assay'],
                      exact_locator=s['locator'],reported_peak_area_percent=reported_pct,
                      value_semantics='GC_MS_PEAK_AREA_PERCENT_NOT_MASS_FRACTION',
                      source_disjoint_from_archived_citation='YES',
                      posthoc_target_selected='YES',
                      blind_independent_gold='NO',
                      eligibility='DEVELOPMENT_PILOT_NOT_CONFIRMATORY' if source_id!='EXT_CLOVE_MOL2026' else 'CONTEXT_REVIEW_REQUIRED',
                      curated_by='AI_ASSISTED_SINGLE_CURATOR',
                      independent_review_1='',independent_review_2='',adjudicated_gold='',
                      limitation='Positive chemical occurrence from this particular extract only; neither universal plant composition nor clinical efficacy inferred.'))
writecsv(OUT/'P2_EXTERNAL_SOURCE_DISJOINT_PILOT_11.csv',panel)

# Source-context trap: the cited Curcuma leaf paper places curzerenone under
# C. angustifolia, not in the C. aromatica rows. This is NOT an absence claim.
traps=[dict(case_id='CTX001',source_id='EXT_CURCUMA_LEAF_2022',herb='Curcuma aromatica',
            compound='curzerenone',challenge='Do Table 2 C. aromatica rows report curzerenone?',
            correct_source_specific_answer='NO_THE_TABLE_ENTRY_IS_C_ANGUSTIFOLIA',
            not_implied='Curzerenone is biologically absent from C. aromatica',
            independent_expert_gold='NO',locator='Table 2, separate C. angustifolia rows',
            url='https://pmc.ncbi.nlm.nih.gov/articles/PMC9686912/'),
       dict(case_id='CTX002',source_id='EXT_CITRUS_LONG_2023',herb='Citrus hystrix',
            compound='citronellal',challenge='Does 6.17% peel oil equal the leaf oil 59.9% reported in a different study?',
            correct_source_specific_answer='NO_DIFFERENT_PLANT_PART_AND_SOURCE',
            not_implied='One experiment invalidates the other',
            independent_expert_gold='NO',locator='Table 2; compare external leaf oil only as context',
            url='https://www.ekosfop.or.kr/archive/view_article_pubreader?pid=kjfp-30-3-395')]
writecsv(OUT/'P2_CONTEXT_SPECIFICITY_CHALLENGES.csv',traps)

# Preserve every archived claim and add a properly scoped external evidence
# cross-reference (not an upgrade of the archived citation's verification grade).
corroboration_map={}
for r in panel: corroboration_map.setdefault(r['assertion_id'],[]).append(r)
audit=[]
for r in claims:
    external=corroboration_map.get(r['assertion_id'],[])
    new=dict(r)
    new['archived_source_primary_fulltext_verified']='YES' if r['original_source_claim_screen_grade']=='PRIMARY_FULLTEXT_EXPERIMENT' else 'NO'
    new['new_source_id_pipe']='|'.join(x['source_id'] for x in external)
    new['new_source_claim_locator_pipe']='|'.join(x['exact_locator'] for x in external)
    new['new_source_evidence_is_not_original_source']='YES' if external else 'NOT_APPLICABLE'
    new['source_specific_disposition']='ORIGINAL_SOURCE_UNCHANGED'
    new['claim_scientific_truth_independently_adjudicated']='NO'
    audit.append(new)
writecsv(OUT/'P2_100_CLAIMS_4LEVEL_AUDIT_V12.csv',audit)

# A new taxonomy must not be called a recovered original 35-class mapping.
family_groups={
'PHENYLALKANONE': ['6-gingerol','6-shogaol','zingerone','6-paradol'],
'SESQUITERPENE_HYDROCARBON':['zingiberene','beta-caryophyllene','alpha-humulene'],
'PIPER_AMIDE':['piperine','pellitorine','piperlongumine','piperolein B','guineensine'],
'MONOTERPENE_HYDROCARBON':['limonene','sabinene','alpha-pinene','beta-pinene','gamma-terpinene','beta-phellandrene','p-cymene'],
'ORGANOSULFUR':['allicin','alliin','diallyl sulfide','diallyl disulfide','ajoene'],
'PHENYLBUTENOID_UNRESOLVED':['DMPBD'],
'MONOTERPENOID_ALCOHOL':['terpinen-4-ol','trans-pinocarveol','linalool','geraniol','borneol'],
'PHENYLPROPANOID_ACETATE':['1\'-acetoxychavicol acetate','1\'-acetoxyeugenol acetate','eugenyl acetate'],
'FLAVONOL':['galangin','kaempferol'],
'MONOTERPENE_ETHER':['1,8-cineole'],
'PHENOLIC_ACID':['rosmarinic acid','gallic acid'],
'TRITERPENOID_ACID':['oleanolic acid','ursolic acid'],
'FLAVONE':['luteolin'],
'PHENYLPROPANOID_PHENOL':['eugenol'],
'TRITERPENOID_SAPONIN':['glycyrrhizin','concinnoside A','concinnoside B','concinnoside C','concinnoside D','concinnoside E'],
'FLAVONOID_GLYCOSIDE':['liquiritin'],
'FLAVANONE':['liquiritigenin'],
'CHALCONE':['isoliquiritigenin'],
'ISOFLAVONOID':['glabridin'],
'BENZOATE_OR_CINNAMATE_ESTER':['methyl salicylate','ethyl cinnamate','ethyl p-methoxycinnamate'],
'MONOTERPENE_ALDEHYDE':['citronellal','myrtenal'],
'HYDROLYSABLE_TANNIN':['chebulagic acid','chebulinic acid','corilagin'],
'ELLAGIC_ACID_TYPE':['ellagic acid'],
'MONOTERPENE_KETONE':['fenchone','camphor'],
'PHENYLPROPENYL_ETHER':['myristicin','elemicin','safrole','methyl eugenol','alpha-asarone','beta-asarone','gamma-asarone'],
'BENZOQUINONE':['thymoquinone','thymohydroquinone'],
'MONOTERPENOID_PHENOL':['thymol','carvacrol'],
'NAPHTHOQUINONE':['plumbagin','elliptinone','droserone','zeylanone'],
'DIMERIC_NAPHTHOQUINONE':['3,3\'-biplumbagin'],
'SESQUITERPENOID_KETONE':['curdione','germacrone','curzerenone'],
'PHENOLIC_SESQUITERPENE':['xanthorrhizol']
}
lookup={}
for family,names in family_groups.items():
    for name in names:
        assert name not in lookup,name
        lookup[name]=family
compounds=readcsv(DATA/'P2_COMPOUND_CANONICAL_MAP.csv')
assert len(compounds)==83
assert set(x['archive_label'] for x in compounds)==set(lookup), {'unknown':set(x['archive_label'] for x in compounds)-set(lookup),'unused':set(lookup)-set(x['archive_label'] for x in compounds)}
newtaxonomy=[]
for r in compounds:
    name=r['archive_label'];family=lookup[name]
    newtaxonomy.append(dict(compound_id_internal=r['compound_id_internal'],archive_compound_label=name,
        reconstructed_family_id='NEWFAM_'+family,
        proposed_family=family,
        status='PRELIMINARY_NAME_BASED_NOT_STRUCTURE_ADJUDICATED' if family!='PHENYLBUTENOID_UNRESOLVED' else 'UNRESOLVED_ABBREVIATION_STRUCTURE',
        original_35class_id='',original_35class_recovered='NO',
        pubchem_cid_verified='',chebi_id_verified='',
        isomer_salt_mixture_caution='YES' if any(t in name for t in ('alpha-','beta-','gamma-','trans-','1,8-','DMPBD')) else 'REVIEW_REQUIRED',
        postprocessing_context='PODS_ALKALINE_HYDROLYSIS_PROSAPOGENOLS' if name.startswith('concinnoside') else '',
        reviewer_1='',reviewer_2='',adjudicated_assignment='',
        allowed_in_confirmatory_35class_replication='NO',
        source_note='Curator-proposed chemical family from compound naming; verify molecular structure and authoritative ontology before use.'))
writecsv(OUT/'P2_NEW_CHEMICAL_FAMILY_RECONSTRUCTION_83.csv',newtaxonomy)
writecsv(OUT/'P2_NEW_FAMILY_DEFINITIONS.csv',[dict(family_id='NEWFAM_'+f, working_label=f,compound_count=len(names),
        identity='NEW_RECONSTRUCTION_NOT_ORIGINAL_35',structure_validation='PENDING',human_adjudication='PENDING')
        for f,names in family_groups.items()])

# Freeze 32 old development cases, then append new external source-context review candidates.
prior=readcsv(DATA/'P3_V07_BENCHMARK_ELIGIBILITY.csv')
assert len(prior)==32
reviews=[]
for r in prior:
    reviews.append(dict(case_id=r['case_id'],stratum='EXISTING_DEVELOPMENT_NOT_HOLDOUT',
         question=r['question'],evidence_url='',expected_answer_candidate='',
         allowed_source_ids='',source_disjoint='NOT_APPLICABLE',
         reviewer1_name='',reviewer1_score='',reviewer1_signature='',
         reviewer2_name='',reviewer2_score='',reviewer2_signature='',
         adjudicator_name='',adjudicated_gold='',adjudication_date='',
         benchmark_ready='NO',reason='Old development question; must not be scored as new independent test.'))
for r in panel:
    reviews.append(dict(case_id=r['case_id'],stratum='POSTHOC_EXTERNAL_EVIDENCE_PILOT',
         question=f"Does {r['source_id']} report {r['compound']} in {r['scientific_name']} ({r['plant_part']})?",
         evidence_url=r['source_url'],expected_answer_candidate=f"Article reports {r['reported_peak_area_percent']}% GC-MS peak area, {r['exact_locator']} (AI-curated, NOT gold)",
         allowed_source_ids=r['source_id'],source_disjoint='YES_DOI',
         reviewer1_name='',reviewer1_score='',reviewer1_signature='',
         reviewer2_name='',reviewer2_score='',reviewer2_signature='',
         adjudicator_name='',adjudicated_gold='',adjudication_date='',
         benchmark_ready='NO',reason='Posthoc targeted positive claims selected after seeing target list; cannot be confirmatory holdout.'))
for r in traps:
    reviews.append(dict(case_id=r['case_id'],stratum='SOURCE_CONTEXT_TRAP_DEVELOPMENT',question=r['challenge'],
          evidence_url=r['url'],expected_answer_candidate=r['correct_source_specific_answer'],
          allowed_source_ids=r['source_id'],source_disjoint='YES_SOURCE',
          reviewer1_name='',reviewer1_score='',reviewer1_signature='',reviewer2_name='',reviewer2_score='',reviewer2_signature='',
          adjudicator_name='',adjudicated_gold='',adjudication_date='',benchmark_ready='NO',reason='Source-specific trap, not biological absence gold.'))
writecsv(OUT/'P3_EXPERT_REVIEW_UNFILLED_45_CASES.csv',reviews)

# External source-based panel is positive-only and posthoc; all metrics requiring
# negative examples or two independent human reviewers are blocked.
with open(OUT/'P3_BENCHMARK_ELIGIBILITY_STATUS.json','w',encoding='utf-8') as f:
    json.dump(dict(total_review_candidates=len(reviews),prior_development=32,
        external_positive_claims=len(panel),context_traps=len(traps),
        independent_human_reviewer_count=0,adjudicated_gold_count=0,
        confirmatory_accuracy_permitted=False,
        positive_only_external_pilot=True,
        source_disjoint_test_available_in_principle=True,
        source_disjoint_confirmatory_benchmark_status='NOT_ELIGIBLE_POSTHOC_TARGET_SELECTION_AND_NO_HUMAN_GOLD'),f,indent=2)

with open(OUT/'P2_TAXONOMY_RECOVERY_STATUS.json','w',encoding='utf-8') as f:
    json.dump(dict(recovered_original_35=False,original_claimed_count=35,original_assignment_mapping_available=False,
        historical_replication_permitted=False,replacement_family_count=len(family_groups),
        replacement_compound_count=len(newtaxonomy),replacement_status='NEW_PRELIMINARY_NOT_STRUCTURE_VALIDATED',
        archive_search='Prior v0.9 WebApp and v0.4 archives had metadata count but no original mapping; no reverse inference'),f,indent=2)
with open(OUT/'P2_ORIGINAL_SOURCE_STATUS.json','w',encoding='utf-8') as f:
    json.dump(dict(total=len(claims),grades=dict(Counter(x['original_source_claim_screen_grade'] for x in claims)),
        original_primary_fulltext=sum(x['archived_source_primary_fulltext_verified']=='YES' for x in audit),
        new_source_supported_distinct_assertions=len({x['assertion_id'] for x in panel}),
        new_source_claims_not_original_source=True,independent_expert_certification=False),f,indent=2)
with open(OUT/'P3_PROJECTION_INPUT_CHECK.json','w',encoding='utf-8') as f:
    json.dump({m:len(Graph().parse(DATA/f'P3_{m}.ttl',format='turtle')) for m in ('M1','M2','M3')},f,indent=2)
print('P2 original source grades:',Counter(x['original_source_claim_screen_grade'] for x in claims))
print('P2 chemical families',len(family_groups),'83 compounds')
print('External positive source-specific claims',len(panel),'case review candidates',len(reviews))
