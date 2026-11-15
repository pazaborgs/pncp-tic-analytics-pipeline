"""Ponto de entrada (Orquestrador) do pipeline de dados PNCP."""

import argparse
import logging

from src.classification.evaluate_sample import evaluate_classifier
from src.classification.run_classification import run_classification
from src.ingest.ingest_pncp import extract_contracts
from src.ingest.to_parquet import convert_raw_to_bronze
from src.load.load_to_bigquery import load_to_bigquery

logger = logging.getLogger(__name__)


def main(skip_ingest: bool = False) -> None:
    """Executa o fluxo sequencial de ingestão, classificação e carga no BigQuery."""
    if not skip_ingest:
        extract_contracts()
        convert_raw_to_bronze()

    run_classification()
    evaluate_classifier()
    load_to_bigquery()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ELT PNCP Santos/SP")
    parser.add_argument(
        "--skip-ingest",
        action="store_true",
        help="Pula a extração da API e conversão Parquet, executando apenas IA e carga no BigQuery.",
    )
    args = parser.parse_args()
    main(skip_ingest=args.skip_ingest)
