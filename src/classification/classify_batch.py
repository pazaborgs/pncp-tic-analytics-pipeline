"""Classificação em lote de objetos de compra via Google GenAI."""

import json

from google import genai
from google.genai import types
from google.genai.errors import APIError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.classification.prompts import SYSTEM_PROMPT
from src.classification.schemas import BatchClassification


@retry(
    retry=retry_if_exception_type(APIError),
    wait=wait_exponential(multiplier=2, min=5, max=60),
    stop=stop_after_attempt(5),
    reraise=True,
)
def classify_batch(
    client: genai.Client,
    records: list[dict],
    llm_config: dict,
) -> list[dict]:
    """Envia um lote de contratações ao LLM e retorna a classificação estruturada.

    Args:
        client: Cliente autenticado do Google GenAI.
        records: Lista de dicts com 'numero_controle_pncp' e 'objeto_compra'.
        llm_config: Parâmetros de modelo e temperatura do config.yaml.

    Returns:
        Lista de dicionários validados pelo schema ClassifiedItem.
    """
    prompt_payload = json.dumps(records, ensure_ascii=False)

    response = client.models.generate_content(
        model=llm_config["model_name"],
        contents=f"Classifique a lista de contratações a seguir:\n{prompt_payload}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=llm_config["temperature"],
            response_mime_type="application/json",
            response_schema=BatchClassification,
        ),
    )

    parsed = BatchClassification.model_validate_json(response.text or "{}")
    return [item.model_dump() for item in parsed.itens]


if __name__ == "__main__":
    from src.utils.llm_client import get_llm_client
    from src.utils.load_config import load_config

    config = load_config()
    client = get_llm_client()

    amostra_teste = [
        {
            "numero_controle_pncp": "TESTE-01",
            "objeto_compra": "Aquisição de monitores multiparamétricos para o centro cirúrgico.",
        },
        {
            "numero_controle_pncp": "TESTE-02",
            "objeto_compra": "Contratação de subscrição de licenças Microsoft 365 e suporte em nuvem.",
        },
        {
            "numero_controle_pncp": "TESTE-03",
            "objeto_compra": "Aquisição de brindes para o evento do Dia do Servidor Público.",
        },
    ]

    resultado = classify_batch(client, amostra_teste, config["llm"])
    for item in resultado:
        print(item)
