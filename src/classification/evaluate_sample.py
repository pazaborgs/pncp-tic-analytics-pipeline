"""Avaliação estatística por amostragem estratificada do classificador de TIC."""

import logging
import math
from pathlib import Path

import pandas as pd

from src.utils.load_config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Auditoria humana sobre a amostra estratificada (random_state=42, n=10 por estrato)
STRATA_AUDIT = {
    "Software e Licenciamento": {"sample_size": 10, "binary_hits": 8, "exact_hits": 8},
    "Redes, Cloud e Segurança": {"sample_size": 10, "binary_hits": 10, "exact_hits": 9},
    "Serviços de TI": {"sample_size": 10, "binary_hits": 8, "exact_hits": 8},
    "Hardware e Equipamentos": {"sample_size": 10, "binary_hits": 9, "exact_hits": 9},
    "Não-TIC": {"sample_size": 10, "binary_hits": 10, "exact_hits": 10},
}


def evaluate_classifier() -> dict[str, float]:
    """Calcula métricas de precisão estratificada e erro padrão sobre o Parquet classificado.

    Returns:
        Dicionário com precisão positiva ponderada, fidelidade de subcategoria,
        acurácia global e margem de erro.
    """
    config = load_config()
    parquet_ia = Path(config["llm"]["output_parquet_path"])
    df_ia = pd.read_parquet(parquet_ia).drop_duplicates(subset=["numero_controle_pncp"])

    counts = df_ia["categoria_tic"].value_counts().to_dict()
    total_pop = len(df_ia)
    tic_cats = [c for c in STRATA_AUDIT if c != "Não-TIC"]
    total_tic = sum(counts.get(c, 0) for c in tic_cats)

    weighted_tic_precision = 0.0
    variance_sum = 0.0

    for cat in tic_cats:
        n_h = counts.get(cat, 0)
        w_h = n_h / total_tic if total_tic else 0.0
        sample_n = STRATA_AUDIT[cat]["sample_size"]
        p_h = STRATA_AUDIT[cat]["binary_hits"] / sample_n

        weighted_tic_precision += w_h * p_h
        # Variância do estimador estratificado: sum(W_h^2 * p_h * (1 - p_h) / (n_h - 1))
        variance_sum += (w_h**2) * (p_h * (1.0 - p_h)) / (sample_n - 1)

    std_error = math.sqrt(variance_sum)
    total_binary_tic_hits = sum(STRATA_AUDIT[c]["binary_hits"] for c in tic_cats)
    total_exact_tic_hits = sum(STRATA_AUDIT[c]["exact_hits"] for c in tic_cats)
    subcategory_fidelity = total_exact_tic_hits / total_binary_tic_hits

    w_non_tic = counts.get("Não-TIC", 0) / total_pop
    w_tic = total_tic / total_pop
    p_non_tic = (
        STRATA_AUDIT["Não-TIC"]["binary_hits"] / STRATA_AUDIT["Não-TIC"]["sample_size"]
    )
    global_accuracy = (w_non_tic * p_non_tic) + (w_tic * weighted_tic_precision)

    metrics = {
        "weighted_tic_precision_pct": round(weighted_tic_precision * 100, 2),
        "standard_error_pct": round(std_error * 100, 2),
        "subcategory_fidelity_pct": round(subcategory_fidelity * 100, 2),
        "global_accuracy_pct": round(global_accuracy * 100, 2),
        "estimated_true_tic_count": round(total_tic * weighted_tic_precision),
    }

    logger.info(
        "Auditoria IA (n=50) | Precisão Ponderada TIC: %s%% (±%s%%) | Fidelidade Subcategoria: %s%% | Acurácia Global: %s%%",
        metrics["weighted_tic_precision_pct"],
        metrics["standard_error_pct"],
        metrics["subcategory_fidelity_pct"],
        metrics["global_accuracy_pct"],
    )
    return metrics


if __name__ == "__main__":
    evaluate_classifier()
