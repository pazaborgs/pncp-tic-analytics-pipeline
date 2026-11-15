## Features da Engenharia de Dados

- `config.yaml` com parâmetros para ingestão, storage, load e camadas do BigQuery.
- Script para ingestão de dados do endpoint de contratações do PNCP (`ingest_pncp.py`):
    - Sessão HTTP resiliente usando objeto `Session` e objeto `Retry` (atrelado a um `HTTPAdapter`).
    - Cálculo das janelas semestrais como parâmetro de busca para o endpoint.
    - `logging` estruturado para acompanhamento de status e erros.
- Script para converter `raw` em Parquet (`to_parquet.py`):
    - Expande os arquivos JSON da camada `raw` para gerar um Parquet consolidado por `load_date`, sendo uma linha por contratação.
    - Adiciona colunas de metadados de engenharia (`_load_date`, `_source_file`, `_ingested_at`).
    - Adiciona coluna de hash SHA-256 (`_row_hash`) para idempotência e carga incremental (`WRITE_APPEND`) posterior.
- IaC usando Terraform para provisionamento no BigQuery, criando 3 datasets (`bronze_pncp`, `stg_pncp`, `marts_pncp`).
- Classificação semântica de TIC com IA (`src/classification/`):
    - Lê os pares únicos `(numeroControlePNCP, objetoCompra)` do Parquet da camada `bronze` e filtra apenas IDs ainda não classificados (`classificacao_tic_ia.parquet`).
    - Envia lotes (`batch_size: 50`) para o modelo `gemini-3.5-flash-lite` usando *Structured Outputs* (`Pydantic`) para garantir o retorno estrito nas 5 categorias do projeto (+75,6% de sensibilidade na detecção de TIC em relação ao filtro léxico por Regex).
    - Salva checkpoints em Parquet a cada lote processado, com controle de *rate limit* e *retry* automático (`tenacity`) para operar dentro do Free Tier.
    - Validação estatística por amostragem aleatória estratificada (`evaluate_sample.py`, `random_state=42`, $n=50$ sendo 10 por estrato): **89,2% de Precisão Positiva Ponderada** ($\pm 4,6\%$ de erro padrão), **97,1% de Fidelidade de Subcategoria** entre os verdadeiros positivos e **99,26% de Acurácia Global Ponderada** na base completa, retroalimentando o `SYSTEM_PROMPT` com os casos de fronteira identificados na auditoria.
    - Análise de assimetria estatística na camada analítica: identificação do Efeito Pareto nas compras públicas de TIC (Ticket Médio de R$ 604,6 mil puxado por 6 contratos plurianuais que concentram 60% do orçamento vs. Mediana real de R$ 15,0 mil) e diferenciação entre Média Simples (`AVG`) e Deságio Médio Ponderado (`SUM(desagio_absoluto) / SUM(valor_total_estimado)`).
- Script para carregar Parquet no BigQuery (`load_to_bigquery.py`):
    - Função genérica de delta (`_upload_delta`) que valida idempotência no BigQuery antes da carga (`WRITE_APPEND`).
    - Carrega as contratações na tabela `bronze_contratacoes_publicacao` (validando por `_row_hash`) e as classificações da IA na tabela `bronze_classificacao_tic_ia` (validando por `numero_controle_pncp`).
- Orquestrador central (`main.py`):
    - Executa sequencialmente extração, conversão para Parquet, classificação via IA e carga incremental no BigQuery, com suporte à flag `--skip-ingest`.
- Modelagem no dbt (`staging` e `marts`):
    - `staging` (`stg_contratacoes`): deduplicação de registros (`QUALIFY ROW_NUMBER()`), `LEFT JOIN` com a tabela de classificação da IA (`bronze_classificacao_tic_ia`), casting de tipos e padronização de colunas em `snake_case`, materializado como view no dataset Silver (`stg_pncp`).
    - `marts` (`fct_contratacoes`): engenharia de atributos (cálculo de deságio absoluto/percentual, status do processo, agrupamento de competitividade, porte da contratação e sazonalidade), materializado como tabela física no dataset Gold (`marts_pncp`).
    - Testes de qualidade de dados (`schema.yml` em `staging` e `marts`): 22 testes automatizados (`unique`, `not_null`, `accepted_values`) validando integridade de chave primária e regras de domínio no BigQuery (`dbt test`).

