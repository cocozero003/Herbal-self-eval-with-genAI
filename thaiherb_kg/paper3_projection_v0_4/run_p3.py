from rdflib import Graph
from src.build import build_p3, make_shacl_shapes, build_semantic_controls, run_shacl_if_available, make_dashboard, OUT
if __name__=='__main__':
    build_p3();make_shacl_shapes()
    build_semantic_controls(Graph().parse(OUT/'P3_M3.ttl',format='turtle'))
    run_shacl_if_available()
    make_dashboard('Paper 3 v0.4 | M1, M2, M3 Source-Parity Explorer','P3_ALL_ASSERTIONS_MODEL_RENDERED_624.csv','Paper3_M1M2M3_v0.4.html',
         'Same frozen 208 V3 assertions for each of three representation projections. Output is a rendering smoke test, not question-answer benchmark accuracy.')
    print('Paper 3 v0.4 projection artifacts rebuilt')
