"""Orquestrador de classificação incremental de contratações de TIC com IA."""

import logging
import time
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from src.classification.classify_batch import classify_batch
from src.utils.llm_client import get_llm_client
from src.utils.load_config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_classification() -> int:
    """Classifica contratações pendentes em lotes e persiste checkpoints em Parquet.

    Returns:
        Total de novos registros classificados na execução.
    """
    config = load_config()

    bronze_path = Path(config["storage"]["bronze_path"])
    load_date = max(p.name.split("=")[1] for p in bronze_path.glob("load_date=*"))
    parquet_file = (
        bronze_path / f"load_date={load_date}" / f"contratacoes_{load_date}.parquet"
    )

    df_source = (
        pd.read_parquet(
            parquet_file,
            columns=["numeroControlePNCP", "objetoCompra"],
        )
        .drop_duplicates(subset=["numeroControlePNCP"])
        .rename(
            columns={
                "numeroControlePNCP": "numero_controle_pncp",
                "objetoCompra": "objeto_compra",
            }
        )
    )

    output_path = Path(config["llm"]["output_parquet_path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Filtra apenas IDs que ainda não constam no Parquet de classificações
    if output_path.exists():
        df_existing = pd.read_parquet(output_path)
        classified_ids = set(df_existing["numero_controle_pncp"])
        df_pending = df_source[~df_source["numero_controle_pncp"].isin(classified_ids)]
    else:
        df_existing = pd.DataFrame()
        df_pending = df_source

    if df_pending.empty:
        logger.info("Idempotência validada: 0 contratações novas para classificar.")
        return 0

    client = get_llm_client()
    llm_config = config["llm"]
    batch_size = llm_config["batch_size"]
    records = df_pending.to_dict(orient="records")
    total_batches = (len(records) + batch_size - 1) // batch_size

    logger.info("Iniciando classificação de %s registros em %s lotes.", len(records), total_batches)

    for idx, i in enumerate(range(0, len(records), batch_size), start=1):
        batch = records[i : i + batch_size]
        logger.info("Classificando lote %s/%s (%s itens)...", idx, total_batches, len(batch))

        batch_results = classify_batch(client, batch, llm_config)
        df_batch = pd.DataFrame(batch_results)
        df_batch["_classified_at"] = datetime.now(UTC).isoformat()

        df_existing = pd.concat([df_existing, df_batch], ignore_index=True)
        df_existing.to_parquet(output_path, index=False)

        if idx < total_batches:
            time.sleep(llm_config["rate_limit_sleep_seconds"])

    logger.info("Classificação concluída: %s novos registros salvos em %s.", len(records), output_path)
    return len(records)


if __name__ == "__main__":
    run_classification()
