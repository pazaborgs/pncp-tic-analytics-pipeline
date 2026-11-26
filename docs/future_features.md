# Capítulo Extra e Evolução Futura (Pós-V1)

A **V1 deste projeto está concluída de ponta a ponta** (Ingestão $\rightarrow$ Bronze Parquet $\rightarrow$ Classificação IA validada $\rightarrow$ BigQuery + Terraform $\rightarrow$ dbt Silver/Gold com 22 testes $\rightarrow$ 14 Análises SQL $\rightarrow$ Insights $\rightarrow$ Dashboard Power BI `.pbip`).

Como a premissa central da V1 foi operar **100% dentro do Free Tier** sem custos fixos de servidor na nuvem, os itens abaixo foram planejados como **Capítulo Extra** e **Evolução V2** — e a arquitetura atual já foi desenhada para recebê-los sem refatoração pesada.

---

## 1. Capítulo Extra: Apache Airflow Local (`docker-compose`) + Ingestão Incremental

Hoje o pipeline roda sob demanda via `main.py`, e o `ingest_pncp.py` faz uma extração completa (*Backfill*) desde `2024-01-01` conforme o `config.yaml`. A idempotência já protege tanto a classificação IA (`numero_controle_pncp`) quanto o BigQuery (`_row_hash`), impedindo duplicações.

O próximo capítulo técnico consiste em transformar as etapas do `main.py` em **tasks isoladas com retries no Apache Airflow** rodando localmente via **`docker-compose`** (on-demand, evitando custo de hospedagem 24/7 e lidando naturalmente com a expiração do BigQuery Sandbox) e evoluir a ingestão para modo incremental:

### Estratégia A: Janela Deslizante Fixa (*Sliding Window*)
Adicionar `lookback_days: 7` (ou `15`) no `config.yaml` para buscar sempre os últimos $X$ dias a partir da data atual.
- **Prós:** Simples de implementar e tolera quedas temporárias da API do governo graças à sobreposição de dias.
- **Limitação:** Assume que já existe um backfill histórico prévio no Data Warehouse — se a tabela expirar no BigQuery Sandbox, baixar apenas os últimos 7 dias deixaria o histórico incompleto.

### Estratégia B: Marca D'Água com Margem de Sobreposição (*High Watermark + Overlap*) *(Preferida)*
Antes de chamar a API, o script consulta a última data disponível no BigQuery:
```sql
SELECT MAX(data_publicacao) FROM `pncp-project.stg_pncp.stg_contratacoes`
```
- **Se a tabela não existir (`NotFound`, ex.: primeira execução ou após expiração no Sandbox):** faz *fallback* automático para o `start_date: "2024-01-01"` (backfill completo).
- **Se já existir:** parte de `MAX(data_publicacao) - 15 dias`.
- **Por que subtrair 15 dias em vez de começar no dia imediatamente seguinte?** Porque o endpoint `/v1/contratacoes/publicacao` filtra pela **data de publicação**, enquanto o `valorTotalHomologado` e o status costumam ser atualizados semanas depois. Esse *overlap* captura homologações tardias de editais recentes, enquanto `_row_hash` e `QUALIFY ROW_NUMBER()` deduplicam tudo sem duplicidade.

---

## 2. Evolução V2: Extração de Itens e Vencedores (`/itens` e `/resultados`) apenas para TIC

O endpoint `/v1/contratacoes/publicacao` entrega o cabeçalho e o valor global de cada contratação, mas não detalha itens unitários (marca/modelo de equipamentos, quantidade exata de licenças) nem o CNPJ do fornecedor vencedor. No PNCP, esses dados vivem em sub-rotas individuais por processo (`/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens` e `/resultados`).

- **Por que não baixar na V1:** Fazer mais de 5.176 requisições individuais para todo o município seria lento e pesado.
- **Como a IA da V1 viabiliza a V2:** Como já isolamos exatamente os **353 processos de TIC** em `bronze_classificacao_tic_ia`, um futuro extrator precisa fazer apenas ~353 chamadas (menos de 7% da base original) para destravar auditoria de **preço unitário por equipamento** e **concentração de mercado por CNPJ vencedor**.
