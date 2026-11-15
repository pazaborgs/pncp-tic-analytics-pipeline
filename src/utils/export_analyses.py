"""Executa as análises compiladas do dbt no BigQuery e consolida os resultados em Markdown."""

import logging
import os
import shutil
import subprocess
from decimal import Decimal
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery

from src.utils.load_config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def _format_cell(val: object) -> str:
    """Formata células para leitura humana em Markdown (pt-BR)."""
    if val is None or pd.isna(val):
        return ""
    if isinstance(val, (Decimal, float)) and not isinstance(val, bool):
        formatted = f"{val:,.2f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return str(val).replace("\n", " ").replace("\r", " ").replace("|", "/")


def _df_to_markdown(df: pd.DataFrame) -> str:
    """Converte um DataFrame em tabela Markdown sem dependências externas."""
    if df.empty:
        return "_Nenhum registro retornado._"

    headers = [str(col).lower() for col in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for row in df.itertuples(index=False, name=None):
        cells = [_format_cell(val) for val in row]
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def export_analyses() -> Path:
    """Compila as análises do dbt, executa no BigQuery e salva o relatório consolidado.

    Returns:
        Caminho do arquivo Markdown gerado em dbt_pncp/analyses/.
    """
    load_dotenv()
    config = load_config()
    project_id = os.getenv(config["bigquery"]["env_project_var"], "pncp-project")

    compiled_dir = Path("dbt_pncp/target/compiled/dbt_pncp/analyses")
    shutil.rmtree(compiled_dir, ignore_errors=True)

    logger.info("Compilando modelos e análises do dbt...")
    subprocess.run(
        ["dbt", "compile", "--project-dir", "dbt_pncp"],
        check=True,
    )

    sql_files = sorted(compiled_dir.rglob("*.sql"))

    client = bigquery.Client(project=project_id)
    report_sections = [
        "# Resultados Consolidados das Análises SQL (`marts_pncp.fct_contratacoes`)",
        "",
        f"Total de consultas executadas: **{len(sql_files)}**",
        "",
    ]

    for sql_file in sql_files:
        rel_name = sql_file.relative_to(compiled_dir).as_posix()
        logger.info("Executando %s...", rel_name)
        query = sql_file.read_text(encoding="utf-8")
        df = client.query(query).to_dataframe()

        report_sections.extend([
            f"## `{rel_name}` ({len(df)} linhas)",
            "",
            _df_to_markdown(df),
            "",
            "---",
            "",
        ])

    output_path = Path("dbt_pncp/analyses/resultados_analises.md")
    output_path.write_text("\n".join(report_sections), encoding="utf-8")
    logger.info("Relatório consolidado salvo em %s", output_path)
    return output_path


if __name__ == "__main__":
    export_analyses()
