"""Módulo de Conversão da Camada Raw (JSON) para Bronze (Parquet).

Consolida os arquivos JSON paginados da última carga (load_date) em um único
arquivo Parquet unificado, calculando o hash SHA-256 por registro e injetando
metadados de linhagem.
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

from src.utils.load_config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def generate_record_hash(record: dict[str, Any]) -> str:
    """Calcula o hash SHA-256 determinístico de um registro bruto da API.

    Args:
        record: Dicionário contendo os dados originais de uma contratação.

    Returns:
        String hexadecimal do hash SHA-256.
    """
    canonical_json = json.dumps(record, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def convert_raw_to_bronze() -> int:
    """Converte todos os JSONs da última partição load_date em um Parquet consolidado.

    Localiza a pasta load_date mais recente na camada raw, desempacota a chave
    'data', gera o hash de conteúdo (_row_hash), achata estruturas aninhadas
    e salva o dataset deduplicado na camada bronze.

    Returns:
        Quantidade total de registros únicos gravados no arquivo Parquet.
    """
    config = load_config()

    raw_data_path = Path(config["storage"]["raw_data_path"])
    bronze_path = Path(config["storage"]["bronze_path"])

    # Identifica a partição de carga (load_date) mais recente na camada raw
    load_date = max(p.name.split("=")[1] for p in raw_data_path.glob("load_date=*"))
    last_load_dir = raw_data_path / f"load_date={load_date}"

    json_files = sorted(last_load_dir.rglob("*.json"))
    if not json_files:
        logger.warning("Nenhum arquivo JSON encontrado em %s", last_load_dir)
        return 0

    full_records: list[dict[str, Any]] = []
    ingested_at = pd.Timestamp.now().isoformat()

    for file_path in json_files:
        with file_path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        records = payload.get("data", [])
        for record in records:
            # Calcula o hash sobre o dado original antes de adicionar metadados técnicos
            record_hash = generate_record_hash(record)
            record["_row_hash"] = record_hash
            record["_load_date"] = load_date
            record["_source_file"] = str(file_path.relative_to(raw_data_path))
            record["_ingested_at"] = ingested_at
            full_records.append(record)

    if not full_records:
        return 0

    # Achata dicionários aninhados (ex.: orgaoEntidade_cnpj) e remove duplicatas intra-lote
    df = pd.json_normalize(full_records, sep="_")
    df = df.drop_duplicates(subset=["numeroControlePNCP", "_row_hash"]).reset_index(
        drop=True
    )

    output_dir = bronze_path / f"load_date={load_date}"
    output_file = output_dir / f"contratacoes_{load_date}.parquet"
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_file, index=False)

    logger.info(
        "Bronze gerada: %s | Registros únicos: %s | Colunas: %s",
        output_file.relative_to(bronze_path),
        len(df),
        df.shape[1],
    )

    return len(df)


if __name__ == "__main__":
    convert_raw_to_bronze()
