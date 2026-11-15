"""Módulo de Carga Incremental (Delta) da Camada Bronze para o BigQuery."""

import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

from src.utils.load_config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def _upload_delta(
    client: bigquery.Client,
    parquet_file: Path,
    table_id: str,
    key_column: str,
    write_disposition: str,
) -> int:
    """Envia ao BigQuery apenas registros cuja chave ainda não consta na tabela destino.

    Args:
        client: Cliente autenticado do BigQuery.
        parquet_file: Caminho do arquivo Parquet local.
        table_id: Identificador completo da tabela (project.dataset.table).
        key_column: Nome da coluna usada para verificação de idempotência.
        write_disposition: Política de escrita do Load Job (ex: WRITE_APPEND).

    Returns:
        Quantidade de registros inéditos carregados.
    """
    if not parquet_file.exists():
        logger.warning("Arquivo %s não encontrado. Pulando carga.", parquet_file)
        return 0

    df = pd.read_parquet(parquet_file)
    logger.info("Lido Parquet local: %s (%s registros)", parquet_file.name, len(df))

    try:
        query = f"SELECT DISTINCT {key_column} FROM `{table_id}`"
        existing_keys = {row[key_column] for row in client.query(query).result()}
        df_delta = df[~df[key_column].isin(existing_keys)]
    except NotFound:
        logger.info("Tabela %s não existe. Preparando carga inicial completa.", table_id)
        df_delta = df

    if df_delta.empty:
        logger.info("Idempotência validada em %s: 0 novos registros.", table_id)
        return 0

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=write_disposition,
    )

    logger.info("Enviando delta de %s registros para %s...", len(df_delta), table_id)
    load_job = client.load_table_from_dataframe(
        df_delta,
        destination=table_id,
        job_config=job_config,
    )
    load_job.result()

    logger.info("Sucesso! %s registros carregados em %s.", len(df_delta), table_id)
    return len(df_delta)


def load_to_bigquery() -> dict[str, int]:
    """Executa a carga incremental das tabelas Bronze (contratações e classificação IA).

    Returns:
        Dicionário com o total de registros inseridos em cada tabela.
    """
    load_dotenv()
    config = load_config()

    project_id = os.getenv(config["bigquery"]["env_project_var"], "pncp-project")
    dataset_id = config["bigquery"]["datasets"]["bronze"]
    tables_cfg = config["bigquery"]["tables"]
    write_disposition = config["bigquery"]["load_job"]["write_disposition"]

    client = bigquery.Client(project=project_id)

    # 1. Parquet mais recente de contratações
    bronze_path = Path(config["storage"]["bronze_path"])
    load_date = max(p.name.split("=")[1] for p in bronze_path.glob("load_date=*"))
    parquet_contratacoes = (
        bronze_path / f"load_date={load_date}" / f"contratacoes_{load_date}.parquet"
    )
    table_contratacoes = f"{project_id}.{dataset_id}.{tables_cfg['contratacoes_bronze']}"

    # 2. Parquet acumulativo de classificação de TIC via IA
    parquet_ia = Path(config["llm"]["output_parquet_path"])
    table_ia = f"{project_id}.{dataset_id}.{tables_cfg['classificacao_tic_bronze']}"

    inserted_contratacoes = _upload_delta(
        client=client,
        parquet_file=parquet_contratacoes,
        table_id=table_contratacoes,
        key_column="_row_hash",
        write_disposition=write_disposition,
    )

    inserted_ia = _upload_delta(
        client=client,
        parquet_file=parquet_ia,
        table_id=table_ia,
        key_column="numero_controle_pncp",
        write_disposition=write_disposition,
    )

    return {
        "contratacoes": inserted_contratacoes,
        "classificacao_tic_ia": inserted_ia,
    }


if __name__ == "__main__":
    load_to_bigquery()
