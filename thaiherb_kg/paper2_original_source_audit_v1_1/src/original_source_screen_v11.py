"""Traceable, conservative source screening for a frozen 100-assertion corpus.

This is a literature *screen*, not full-text verification for every record.
A positive abstract match does not establish a full-text analytical match.
An older review's mention is classified separately from direct experiments.
"""
from __future__ import annotations
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RESULTS = ROOT / 'results'
DATE = '2026-11-07'
SOURCE_INFO = {
 'SRC_GINGER': ('REVIEW', 'https://www.mdpi.com/2304-8158/8/6/185', 'Mao et al. (2019), Foods 8(6),185', 'Review of ginger metabolites; constituent-specific primary analytical findings not attributable to the authors.'),
 'SRC_RETRO': ('PRIMARY_ANALYTICAL', 'https://doi.org/10.3390/antiox10101642','Luca et al. (2021), Antioxidants 10(10),1642', 'Original Piper species analysis, source article Table 3; audited five rows in v0.6.'),
 'SRC_BLACK': ('REVIEW', 'https://link.springer.com/article/10.1186/s40816-021-00292-2', 'Ashokkumar et al. (2021), Clinical Phytoscience 7,52','Original paper is a review of seed oil and piperine; tables synthesize multiple studies.'),
 'SRC_GARLIC': ('REVIEW', 'https://www.mdpi.com/2304-8158/8/7/246', 'Shang et al. (2019), Foods 8(7),246','Section 2 is a review of organosulfur compounds; no original chemistry assay.'),
 'SRC_PLAI': ('PRIMARY_ANALYTICAL', 'https://doi.org/10.1002/jsfa.8474', 'Verma et al. (2018), J Sci Food Agric 98,321-327','Original rhizome essential oil was hydrodistilled and analyzed using GC-FID/GC-MS; five analytes stated in abstract.'),
 'SRC_GALANGAL': ('REVIEW_GENUS', 'https://pubs.rsc.org/en/content/articlehtml/2017/ra/c6ra27830b', 'Ma et al. (2017), RSC Advances 7,14114-14144', 'Genus-level Alpinia review, not solely Alpinia galanga and not direct analysis.'),
 'SRC_BASIL': ('REVIEW', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11521583/', 'Bhattarai et al. (2024), TheScientificWorldJournal 2024,8895039', 'Ocimum tenuiflorum review; authors summarize other studies.'),
 'SRC_LICORICE': ('REVIEW', 'https://doi.org/10.3390/plants10122751', 'Plants (2021) 10,2751', 'Comprehensive review of Glycyrrhiza glabra phytochemistry and pharmacology.'),
 'SRC_CLOVE': ('REVIEW', 'https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2022.1002147/full', 'Frontiers in Nutrition (2022), 1002147', 'Review; Sec. Aromatics and Terpenoids recapitulates older assays.'),
 'SRC_KAFFIR': ('REVIEW', 'https://arabjchem.org/citrus-hystrix-a-review-of-phytochemistry-pharmacology-and-industrial-applications-research-progress/', 'Zhao et al. (2023), Arabian Journal of Chemistry 16,105236', 'Review of Citrus hystrix across plant parts and processes; no single assay.'),
 'SRC_CHEBULA': ('REVIEW', 'https://pubmed.ncbi.nlm.nih.gov/39683707/', 'Wang et al. (2024), Molecules 29(23),5547', 'Review of Terminalia chebula fruit.'),
 'SRC_CARDAMOM': ('PRIMARY_ANALYTICAL', 'https://agris.fao.org/search/en/providers/122535/records/65de2c640f3e94b9e5cb6f69', 'Sirat et al. (2001), Journal of Essential Oil Research 13,86-87', 'Original Amomum testaceum fruit hydrodistillate GC/GC-MS/IR/NMR; source uses synonym of Wurfbainia testacea.'),
 'SRC_NUTMEG': ('REVIEW', 'https://pubmed.ncbi.nlm.nih.gov/28082856/', 'Abourashed & El-Alfy (2016), Phytochemistry Reviews 15,1035-1056', 'Review of Myristica fragrans metabolites; distinguish seed and aril.'),
 'SRC_CORIANDER': ('REVIEW', 'https://pubmed.ncbi.nlm.nih.gov/36677754/', 'Al-Khayri et al. (2023), Molecules 28(2),696', 'Review of Coriandrum sativum essential oil.'),
 'SRC_NIGELLA': ('REVIEW', 'https://pubmed.ncbi.nlm.nih.gov/39769174/', 'Alberts et al. (2024), Int J Mol Sci 25,13410', 'Review of Nigella sativa compounds and applications.'),
 'SRC_KAEMPFERIA': ('REVIEW', 'https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2021.675350/full', 'Wang et al. (2021), Front Pharmacol 12,675350', 'Review has Table 3 chemical inventory and Table 4 oil constituents across origins; material not interchangeable.'),
 'SRC_ACORUS': ('REVIEW_GENUS', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10609487/', 'Zhao et al. (2023), Molecules 28,7117', 'Genus-wide Acorus review; each chemical must be linked to specific species.'),
 'SRC_PLUMBAGO': ('PRIMARY_WITH_BACKGROUND', 'https://www.nature.com/articles/s41598-022-13718-9', 'Selim et al. (2022), Scientific Reports, DOI 10.1038/s41598-022-13718-9', 'Original analytical and animal study, but species metabolite names in introduction refer to earlier publications; not automatically direct Table 1 detections.'),
 'SRC_SOMPOI': ('PRIMARY_ANALYTICAL', 'https://www.jstage.jst.go.jp/article/cpb1958/45/4/45_4_620/_article/-char/en', 'Gafur et al. (1997), Chem Pharm Bull 45(4),620-625', 'Primary structure elucidation of prosapogenols in alkaline-hydrolyzed pod saponin fraction, not necessarily native intact plant molecules.'),
 'SRC_CURCUMA': ('REVIEW_GENUS', 'https://pubmed.ncbi.nlm.nih.gov/30200410/', 'Dosoky & Setzer (2018), Nutrients 10,1196', 'Review spans several Curcuma species; species-resolved evidence required for C. aromatica.'),
}

# Specific claim checks supported by located primary source abstract or review sections.
# Unknown claims remain pending, not 'false'.
MATCH = {}
def add(ids, grade, locator, context, note=''):
    for id_ in ids:
        if id_ in MATCH: raise ValueError('Duplicate claim mapping: '+id_)
        MATCH[id_] = (grade, locator, context, note)

add([f'CA{i:03d}' for i in range(6,11)], 'PRIMARY_FULLTEXT_EXPERIMENT', 'Luca et al. 2021, section 3.1/Table 3', 'Methanolic Piper retrofractum fruit extract / LC-based chemical analysis', 'Prior claim-by-claim author-audited v0.6 original source; not expert independent.')
add([f'CA{i:03d}' for i in range(21,26)], 'PRIMARY_ABSTRACT_EXPERIMENT', 'Verma et al. 2018 abstract, RESULTS', 'Zingiber montanum rhizome hydrodistilled essential oil; GC-FID and GC-MS', 'Five constituents and ranges; original paper full-text table not rechecked.')
add([f'CA{i:03d}' for i in range(56,61)], 'PRIMARY_ABSTRACT_EXPERIMENT', 'Sirat et al. 2001 abstract as indexed by FAO AGRIS', 'Amomum testaceum (= Wurfbainia testacea) fruit oil; hydrodistillation and GC/GC-MS/IR/NMR', 'Chemical quantities refer to analyzed fruit oil; not a general species composition constant.')
add([f'CA{i:03d}' for i in range(91,96)], 'PRIMARY_ABSTRACT_PROCESS_DEPENDENT', 'Gafur et al. 1997 abstract (J-STAGE)', 'Acacia concinna (= Senegalia rugata) pods: alkaline hydrolysis of highly polar saponin fraction', 'Concinnosides A-E were characterized from hydrolysate. Do not assert unqualified native presence.')
add([f'CA{i:03d}' for i in range(11,16)], 'SECONDARY_FULLTEXT_REVIEW', 'Ashokkumar et al. 2021, section Essential oil/Oleoresin/Piperine, Tables 2-3', 'Piper nigrum piperine and seed/leaf essential oils; synthesis across original studies', 'Mentions compounds, not new direct study; source origin and plant part vary.')
add([f'CA{i:03d}' for i in range(16,21)], 'SECONDARY_FULLTEXT_REVIEW', 'Shang et al. 2019, section 2 Bioactive Compounds of Garlic', 'Allium sativum summary of organosulfur chemistry; preparation changes stability', 'Review mention not primary measurement; allicin/alliin transformation risk.')
add([f'CA{i:03d}' for i in range(76,81)], 'SECONDARY_FULLTEXT_REVIEW', 'Wang et al. 2021, chemistry Table 3 / essential oil Table 4', 'Kaempferia galanga: various origins, distillation methods, rhizome essential oil', '1,8-cineole is also eucalyptol; not a new original assay.')
add([f'CA{i:03d}' for i in range(41,45)], 'SECONDARY_FULLTEXT_REVIEW', 'Frontiers in Nutrition 2022, sections Aromatics/Terpenoids', 'Syzygium aromaticum review of essential oil constituents', 'Methyl salicylate CA045 remains not claim-specific verified.')

TAXONOMY = [
 {'herb_id':'H12','accepted_name':'Wurfbainia testacea (Ridl.) Škorničk. & A.D.Poulsen','name_in_older_source':'Amomum testaceum Ridl.','relationship':'homotypic_synonym','authority':'Royal Botanic Gardens, Kew, Plants of the World Online','url':'https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:77178292-1','note':'2018 accepted recombination; supports linking 2001 experimental paper. Do not normalize different Amomum species.'},
 {'herb_id':'H19','accepted_name':'Senegalia rugata (Lam.) Britton & Rose','name_in_older_source':'Acacia concinna (Willd.) DC.','relationship':'heterotypic_synonym','authority':'Royal Botanic Gardens, Kew, Plants of the World Online','url':'https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:518300-1','note':'Kew synonym accepted; 1997 pod hydrolysis does not imply untreated pod occurrence.'},
]


def records(path):
    with path.open(newline='', encoding='utf-8-sig') as stream:
        return list(csv.DictReader(stream))


def write(path, rows):
    if not rows: raise ValueError('no records')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def run():
    RESULTS.mkdir(exist_ok=True)
    locked = DATA / 'P2_CHEM_EVIDENCE_100_v05_LOCKED.csv'
    original = records(locked)
    assert len(original)==100 and len(set(r['assertion_id'] for r in original))==100
    assert len(SOURCE_INFO)==20
    assert len(set(r['source_id'] for r in original))==20
    assert len(MATCH)==39
    audit=[]
    for r in original:
        sid=r['source_id']
        kind,url,ref,scope=SOURCE_INFO[sid]
        grade,loc,context,note=MATCH.get(r['assertion_id'],('UNRESOLVED_CLAIM_LOCATOR','','','No claim-specific source location checked in this release; not evidence of compound absence.'))
        audit.append({
          'assertion_id':r['assertion_id'], 'herb_id':r['herb_id'], 'scientific_name_locked':r['herb_scientific_name'],
          'compound_locked':r['compound_label'], 'source_id_locked':sid, 'original_source_url_locked':r['source_url_from_archive'],
          'original_disposition_immutable':r['disposition'], 'source_type_screened':kind, 'source_type_url':url,
          'original_source_claim_screen_grade':grade, 'locator':loc, 'material_process_context':context, 'limitations':note,
          'source_reading':'AI_ASSISTED_NOT_INDEPENDENT', 'checked_date':DATE, 'source_confirmation_level':'ABSTRACT_OR_FULLTEXT_AS_SPECIFIED',
          'expert_reviewer_1':'', 'expert_reviewer_2':'', 'adjudicated_gold':'', 'external_validation_eligible':'NO_POSTHOC_SOURCE_SCREEN',
        })
    srcs=[]
    for sid,(kind,url,ref,scope) in SOURCE_INFO.items():
        srcs.append({'source_id':sid,'screened_source_type':kind,'source_url':url,
                     'bibliography':ref,'source_scope_note':scope,
                     'scope_of_review':'SOURCE_TYPE_AND_SELECTED_CLAIMS_NOT_ALL_COMPOUNDS',
                     'independent_expert_verified':'NO','review_date':DATE})
    write(RESULTS/'P2_ORIGINAL_SOURCE_TRACE_100_v11.csv', audit)
    write(RESULTS/'P2_SOURCE_TYPE_AUDIT_20_v11.csv', srcs)
    write(RESULTS/'P2_TAXON_SYNONYM_2_v11.csv', TAXONOMY)
    grades=dict(Counter(r['original_source_claim_screen_grade'] for r in audit))
    assert grades=={'UNRESOLVED_CLAIM_LOCATOR':61,'SECONDARY_FULLTEXT_REVIEW':19,
                   'PRIMARY_ABSTRACT_EXPERIMENT':10,'PRIMARY_ABSTRACT_PROCESS_DEPENDENT':5,
                   'PRIMARY_FULLTEXT_EXPERIMENT':5},grades
    output={'release':'Paper2-v1.1', 'total_claims':100,'source_types_screened':20,
            'source_type_counts':dict(Counter(r['screened_source_type'] for r in srcs)),
            'claim_screen_grades':grades,'taxon_synonyms_grounded':2,
            'original_primary_fulltext':5, 'abstract_primary_claims':15,
            'secondary_source_mentions':19,'unresolved_claims':61,
            'expert_adjudicated':0,'primary_source_full_text_for_all_claims':False,
            'frozen_sha256':hashlib.sha256(locked.read_bytes()).hexdigest(),
            'interpretation':'AI-assisted evidence screen; source types and locators are not clinical efficacy or expert validation'}
    (RESULTS/'P2_V11_AUDIT_SUMMARY.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    return output

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
