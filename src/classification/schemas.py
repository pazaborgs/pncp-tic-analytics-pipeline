"""Contratos Pydantic para saída estruturada da classificação de TIC."""

from typing import Literal

from pydantic import BaseModel, Field

TIC_Categories = Literal[
    "Software e Licenciamento",
    "Redes, Cloud e Segurança",
    "Hardware e Equipamentos",
    "Serviços de TI",
    "Não-TIC",
]


class ClassifiedItem(BaseModel):
    """Schema de classificação individual de uma contratação."""

    numero_controle_pncp: str = Field(
        description="PK da contratação recebida na entrada."
    )
    is_tic: bool = Field(description="True se TIC, False caso contrário.")
    categoria_tic: TIC_Categories = Field(description="Categoria da contratação.")


class BatchClassification(BaseModel):
    """Schema da lista de contratações classificadas em um lote."""

    itens: list[ClassifiedItem]
