"""Cliente de conexão com a API Google GenAI."""

from dotenv import load_dotenv
from google import genai


def get_llm_client() -> genai.Client:
    """Inicializa o cliente do Google GenAI lendo GEMINI_API_KEY do ambiente.

    Returns:
        Instância autenticada de genai.Client.
    """
    load_dotenv()
    return genai.Client()
