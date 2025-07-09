import click
from src.evaluator.pipeline import run_pipeline
import json

@click.group()
def cli():
    pass

@cli.command()
@click.option('--input', 'input_path', required=True, help='Path to input JSON schema')
@click.option('--output', 'output_path', required=True, help='Path for output package')
def run(input_path, output_path):
    """Run full pipeline."""
    schema = json.loads(open(input_path).read())
    run_pipeline(schema, output_path)

if __name__ == "__main__":
    cli()
