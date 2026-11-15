"""Módulo de Ingestão de Contratações da API do PNCP.

Realiza a extração paginada de contratações públicas por janela temporal
e modalidade de contratação, persistindo o payload JSON bruto localmente.
"""

import json
import logging
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.load_config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

config = load_config()

# Armazenamento local
raw_data_path = Path(config["storage"]["raw_data_path"])
bronze_path = Path(config["storage"]["bronze_path"])
file_format = config["storage"]["file_format"]

# Conexão, paginação e resiliência
base_url = config["api"]["base_url"]
endpoint = config["api"]["endpoints"]["contratacoes_publicacao"]
headers = config["api"]["headers"]
tamanho_pagina = config["api"]["pagination"]["tamanho_pagina"]
pagina_inicial = config["api"]["pagination"]["pagina_inicial"]
timeout_seconds = config["api"]["resilience"]["timeout_seconds"]
max_retries = config["api"]["resilience"]["max_retries"]
backoff_factor = config["api"]["resilience"]["backoff_factor"]
rate_limit_sleep = config["api"]["resilience"]["rate_limit_sleep_seconds"]

# Escopo e filtros de extração
uf = config["extraction"]["filter_scope"]["uf"]
code_municipio = config["extraction"]["filter_scope"]["codigo_municipio_ibge"]
modalidades = config["extraction"]["modalidades"]
date_range = config["extraction"]["date_range"]


def create_session() -> requests.Session:
    """Cria uma sessão HTTP configurada com estratégia de retry e headers padrão.

    Returns:
        Sessão HTTP do requests pronta para consumo da API.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.headers.update(headers)

    return session


def generate_date_windows(
    start_date_str: str,
    end_date_str: str,
    freq: str = "6MS",
) -> list[tuple[str, str]]:
    """Divide o período de extração em janelas no formato YYYYMMDD exigido pelo PNCP.

    Args:
        start_date_str: Data inicial no formato 'YYYY-MM-DD'.
        end_date_str: Data final no formato 'YYYY-MM-DD' ou 'today'.
        freq: Frequência de divisão das janelas (ex.: '6MS' para início de semestre).

    Returns:
        Lista de tuplas (data_inicial_yyyymmdd, data_final_yyyymmdd).
    """
    start_dt = pd.to_datetime(start_date_str).date()
    end_dt = (
        date.today()
        if end_date_str.lower() == "today"
        else pd.to_datetime(end_date_str).date()
    )

    # Normaliza frequência semestral compatível com pandas
    pd_freq = "6MS" if freq == "6M" else freq
    boundaries = pd.date_range(start=start_dt, end=end_dt, freq=pd_freq).date.tolist()

    if not boundaries or boundaries[0] > start_dt:
        boundaries.insert(0, start_dt)

    windows: list[tuple[str, str]] = []
    for idx, window_start in enumerate(boundaries):
        if idx + 1 < len(boundaries):
            window_end = boundaries[idx + 1] - pd.Timedelta(days=1)
        else:
            window_end = end_dt

        windows.append((window_start.strftime("%Y%m%d"), window_end.strftime("%Y%m%d")))

    return windows


def extract_data(response_json: dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
    """Extrai a lista de registros do payload de resposta da API.

    Args:
        response_json: Objeto JSON retornado pela API do PNCP.

    Returns:
        Lista de dicionários contendo as contratações da página.

    Raises:
        ValueError: Se o formato da resposta não contiver uma lista válida.
    """
    if isinstance(response_json, list):
        return response_json

    if isinstance(response_json, dict):
        records = response_json.get("data", [])
        if isinstance(records, list):
            return records

    raise ValueError("Formato inesperado de resposta da API")


def fetch_window_pages(
    session: requests.Session,
    output_dir: Path,
    load_date: str,
    modalidade_id: int,
    data_inicial: str,
    data_final: str,
) -> int:
    """Extrai todas as páginas de uma combinação de modalidade e janela temporal.

    Args:
        session: Sessão HTTP ativa.
        output_dir: Diretório raiz da camada raw.
        load_date: Data da execução no formato 'YYYY-MM-DD'.
        modalidade_id: Código da modalidade de contratação no PNCP.
        data_inicial: Data inicial no formato 'YYYYMMDD'.
        data_final: Data final no formato 'YYYYMMDD'.

    Returns:
        Total de registros extraídos na janela.
    """
    page = pagina_inicial
    window_records = 0

    target_dir = output_dir / f"load_date={load_date}" / f"modalidade={modalidade_id}"
    target_dir.mkdir(parents=True, exist_ok=True)

    params: dict[str, Any] = {
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "codigoModalidadeContratacao": modalidade_id,
        "codigoMunicipioIbge": code_municipio,
        "uf": uf,
        "pagina": page,
        "tamanhoPagina": tamanho_pagina,
    }

    while True:
        params["pagina"] = page

        response = session.get(
            f"{base_url}{endpoint}",
            params=params,
            timeout=timeout_seconds,
        )
        response.raise_for_status()

        # Trata retorno vazio (HTTP 204 No Content) quando não há compras no período
        if response.status_code == 204 or not response.content:
            logger.info(
                "Modalidade %s [%s a %s] | Sem registros no período.",
                modalidade_id,
                data_inicial,
                data_final,
            )
            break

        response_json = response.json()
        records = extract_data(response_json)

        if not records:
            break

        # Preserva o payload bruto por modalidade, data de carga, janela e página
        output_file = target_dir / f"{data_inicial}_{data_final}_page_{page:04d}.json"
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(response_json, file, ensure_ascii=False, indent=2)

        window_records += len(records)

        logger.info(
            "Modalidade %s [%s a %s] | Página %s | Registros: %s | Acumulado: %s",
            modalidade_id,
            data_inicial,
            data_final,
            page,
            len(records),
            window_records,
        )

        # Verifica critério de parada da paginação
        total_pages = (
            response_json.get("totalPaginas")
            if isinstance(response_json, dict)
            else None
        )

        if total_pages is not None and page >= total_pages:
            break

        if total_pages is None and len(records) < tamanho_pagina:
            break

        page += 1
        time.sleep(rate_limit_sleep)

    return window_records


def extract_contracts() -> int:
    """Orquestra a extração de contratações do PNCP por modalidade e janela temporal.

    Returns:
        Quantidade total de registros extraídos em toda a execução.
    """
    load_date = datetime.now().strftime("%Y-%m-%d")
    raw_data_path.mkdir(parents=True, exist_ok=True)

    windows = generate_date_windows(
        start_date_str=date_range["start_date"],
        end_date_str=date_range["end_date"],
        freq=date_range.get("window_frequency", "6MS"),
    )
    active_modalidades = [m for m in modalidades if m.get("ativo", True)]

    total_records = 0
    logger.info(
        "Iniciando extração PNCP | Município IBGE: %s | Modalidades: %s | Janelas: %s",
        code_municipio,
        len(active_modalidades),
        len(windows),
    )

    with create_session() as session:
        for mod in active_modalidades:
            mod_id = mod["id"]
            mod_nome = mod["nome"]
            logger.info("Processando modalidade %s - %s", mod_id, mod_nome)

            for start_ymd, end_ymd in windows:
                try:
                    total_records += fetch_window_pages(
                        session=session,
                        output_dir=raw_data_path,
                        load_date=load_date,
                        modalidade_id=mod_id,
                        data_inicial=start_ymd,
                        data_final=end_ymd,
                    )
                except requests.RequestException as error:
                    logger.error(
                        "Erro HTTP na modalidade %s [%s a %s]: %s",
                        mod_id,
                        start_ymd,
                        end_ymd,
                        error,
                    )
                    raise
                except (ValueError, KeyError) as error:
                    logger.error(
                        "Erro de parsing na modalidade %s [%s a %s]: %s",
                        mod_id,
                        start_ymd,
                        end_ymd,
                        error,
                    )
                    raise

    logger.info("Extração finalizada. Total geral de registros: %s", total_records)
    return total_records


if __name__ == "__main__":
    extract_contracts()
