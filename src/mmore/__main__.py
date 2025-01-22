import click

from .run_index import index as run_index
from .run_rag import rag as run_rag
from .run_retriever import retrieve as run_retrieve
from .run_postprocess import postprocess as run_postprocess
from .run_process import process as run_process

from contextlib import contextmanager
import warnings
import sys
import os


@contextmanager
def suppress_warnings_and_stdout():
    # Suppress specific warnings
    warnings.filterwarnings('ignore', category=FutureWarning, message="The input name `inputs` is deprecated*")
    
    pypdfium_message = "-> Cannot close object, library is destroyed. This may cause a memory leak!*"
    # Redirect stdout to devnull to catch pypdfium messages
    old_stdout = sys.stdout
    devnull = open(os.devnull, 'w')
    # Suppress pypdfium warnings
    sys.stdout = devnull
    
    try:
        sys.stdout = devnull
        yield
        
    finally:
        sys.stdout = old_stdout
        devnull.close()

with suppress_warnings_and_stdout():
    pass


@click.group()
def main():
    """CLI for mmore commands."""
    pass

@main.command()
@click.option('--config-file', type=str, required=True, help='Dispatcher configuration file path.')
def process(config_file):
    """Process documents from a directory."""
    run_process(config_file)

@main.command()
@click.option('--config-file', type=str, required=True, help='Path to the configuration file.')
@click.option('--input-data', type=str, required=True, help='Path to the input data.')
def postprocess(config_file, input_data):
    """Run the post-processors pipeline."""
    run_postprocess(config_file, input_data)

@main.command()
@click.option('--config-file', '-c', type=str, required=True, help='Path to the configuration file.')
@click.option('--input-data', '-f', type=str, required=True, help='Path to the JSONL data.')
@click.option('--collection-name', '-n', type=str, required=True, help='Name of the collection to index.')
def index(config_file, input_data, collection_name):
    """Run the indexer."""
    with suppress_warnings_and_stdout():
        run_index(config_file, input_data, collection_name)

@main.command()
@click.option('--config-file', '-c', type=str, required=True, help='Dispatcher configuration file path.')
@click.option('--input-file', '-f', type=str, required=True, help='Path to the input file.')
@click.option('--output-file', '-o', type=str, required=True, help='Path to the output file.')
def retrieve(config_file, input_file, output_file):
    """Retrieve documents for specified queries."""
    run_retrieve(config_file, input_file, output_file)

@main.command()
@click.option('--config-file', type=str, required=True, help='Dispatcher configuration file path.')
def rag(config_file):
    """Run the Retrieval-Augmented Generation (RAG) pipeline."""
    run_rag(config_file)

if __name__ == "__main__":
    main()
