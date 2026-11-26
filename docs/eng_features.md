# Engenharia de Dados — Arquitetura e Decisões Técnicas

Este documento detalha as decisões técnicas implementadas no pipeline, desenhado para operar **100% no Free Tier** (BigQuery Sandbox + Google AI Studio) sem abrir mão de idempotência, testes automatizados e boas práticas de produção.

---

## 1. Configuração Centralizada (`config/config.yaml`)
- Parâmetros de ingestão (município IBGE `3548500`, janelas semestrais, 5 modalidades), caminhos locais (`raw`/`bronze`), datasets do BigQuery (`bronze_pncp`, `stg_pncp`, `marts_pncp`) e parâmetros do LLM (`gemini-3.5-flash-lite`, `batch_size: 50`, `temperature: 0.0`, `rate_limit_sleep_seconds: 4.5`) ficam centralizados em um único arquivo YAML lido por `src/utils/load_config.py`.

## 2. Ingestão Resiliente da API do PNCP (`src/ingest/ingest_pncp.py`)
- Consome o endpoint `/v1/contratacoes/publicacao` dividindo o período (`2024-01-01` até a data atual) em **janelas semestrais** (`6MS`) para respeitar limites de consulta da API pública.
- Sessão HTTP resiliente (`requests.Session` + `HTTPAdapter` + `Retry` com backoff exponencial) e `logging` estruturado para acompanhar páginas e eventuais falhas transitórias.
- Extrai **todas as 5.176 contratações** do município (e não apenas TI) para permitir a comparação analítica entre **TIC vs. Não-TIC** na camada Gold.

## 3. Camada Bronze Local & Idempotência (`src/ingest/to_parquet.py`)
- Os JSONs paginados permanecem preservados na camada `raw` (`load_date=YYYY-MM-DD/modalidade=*/page_*.json`).
- O `to_parquet.py` achata as estruturas aninhadas em um arquivo Parquet consolidado por `load_date` (1 linha por contratação).
- **Idempotência antes dos metadados:** o hash SHA-256 (`_row_hash`) é calculado sobre o payload original da API **antes** da injeção das colunas de linhagem (`_load_date`, `_source_file`, `_ingested_at`). Se um processo não mudou na API, seu hash continua idêntico entre execuções.

## 4. Classificação Semântica com IA em Lote (`src/classification/`)
- Como o PNCP não possui uma flag nativa de tecnologia no cabeçalho do processo e filtros por Regex geram falsos positivos graves (*"monitor multiparamétrico cirúrgico"*, *"Dia do Servidor Público"*, *"licença ambiental"*), o pipeline classifica os objetos em lotes de 50 registros usando `gemini-3.5-flash-lite`.
- **Contratos Estritos (`schemas.py`):** usa *Structured Outputs* via **Pydantic** (`BatchClassification` / `ClassifiedItem`) com `Literal` restrito às 5 categorias do domínio.
- **Desacoplamento e Checkpoints (`run_classification.py`):** lê os pares únicos `(numeroControlePNCP, objetoCompra)` da Bronze e salva as classificações em um Parquet dedicado (`classificacao_tic_ia.parquet`) com checkpoint a cada lote, *rate limit* controlado e *retry* automático (`tenacity`). Como o texto do objeto não muda na homologação, cada ID passa pelo LLM uma única vez — elevando a detecção de TIC em **+75,6%** frente ao Regex (de 201 para 353 processos).
- **Auditoria Estatística (`evaluate_sample.py`):** validação por **Amostragem Aleatória Estratificada** (`random_state=42`, $n = 50$, sendo 10 por estrato), aferindo **89,2% de Precisão Positiva Ponderada** ($\pm 5,97\%$ de erro padrão), **97,1% de Fidelidade de Subcategoria** e **99,26% de Acurácia Global Ponderada** (detalhes em [`ai_evaluation_sample.md`](ai_evaluation_sample.md)). Os casos de fronteira descobertos na auditoria retroalimentaram o `SYSTEM_PROMPT`.

## 5. Infraestrutura (Terraform) e Carga Delta no BigQuery (`terraform/`, `src/load/`)
- **Terraform (`terraform/bigquery.tf`):** provisiona os 3 datasets (`bronze_pncp`, `stg_pncp`, `marts_pncp`) via autenticação *keyless* (ADC — zero chaves JSON em disco), configurando expiração explícita de **50 dias** (`4320000000 ms`) para compatibilidade total com o limite de 60 dias do BigQuery Sandbox.
- **Carga Delta (`load_to_bigquery.py`):** a função genérica `_upload_delta()` consulta as chaves existentes no BigQuery antes de subir (`WRITE_APPEND`), validando contratações por `_row_hash` (`bronze_contratacoes_publicacao`) e classificações por `numero_controle_pncp` (`bronze_classificacao_tic_ia`).
- **Orquestrador (`main.py`):** executa o fluxo completo em sequência e suporta `--skip-ingest` para reconstruir o BigQuery Sandbox em segundos direto dos Parquets locais sem gastar nenhum token novo de IA.

## 6. Modelagem, Qualidade de Dados e Analytics (`dbt_pncp/`, `src/utils/export_analyses.py`, `dashboard/`)
- **Silver (`stg_contratacoes`):** view no dataset `stg_pncp` que faz casting de tipos, padronização em `snake_case`, deduplicação da versão mais recente via `QUALIFY ROW_NUMBER()` (particionado por `numero_controle_pncp` e ordenado por `data_atualizacao_global DESC`) e `LEFT JOIN` com a tabela da IA.
- **Gold (`fct_contratacoes`):** tabela física no dataset `marts_pncp` contendo toda a engenharia de atributos (`desagio_absoluto`, `desagio_percentual` protegido por `SAFE_DIVIDE`, `status_processo`, `grupo_competitividade`, `orgao_esfera_nome`, `porte_contratacao`, `dias_janela_proposta` e atributos de calendário).
- **Data Quality (22 testes):** `schema.yml` em `staging` e `marts` executam 22 testes automatizados (`unique`, `not_null`, `accepted_values`) no `dbt build`.
- **Exportação Reprodutível de Análises (`export_analyses.py`):** compila e executa as 14 queries SQL de `dbt_pncp/analyses/` no BigQuery, gerando o relatório formatado [`resultados_analises.md`](../dbt_pncp/analyses/resultados_analises.md).
- **BI Versionado em Git (`dashboard/`):** projeto Power BI em formato aberto **`.pbip`** (JSON + TMDL) conectado à Gold em modo **Import**, garantindo que o dashboard continue 100% funcional mesmo após a expiração de tabelas no BigQuery Sandbox.
