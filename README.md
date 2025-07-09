# GenAI-Powered Herbal Product Self-Evaluation Pilot

This repository contains a Python-based pipeline to generate a self-evaluation dossier for Thai FDA herbal product registration using Generative AI.

## Structure

- `src/`: Application modules  
- `docs/`: Architecture and regulatory guidelines  
- `data/`: Sample input files  
- `examples/`: Minimal input/output examples  
- `notebooks/`: Prototyping notebooks  
- `tests/`: Unit and integration tests

## Quickstart

```bash
cp .env.example .env
pip install -r requirements.txt
python -m src.cli run --input examples/input_dossier.json --output output_summary.pdf
```