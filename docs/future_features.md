# Roadmap e Ideias de Evolução (Future Features)

Este documento reúne ideias de evolução arquitetural para o projeto. Como a premissa central aqui é operar 100% dentro do **Free Tier** (tanto no BigQuery quanto na API do Gemini), algumas automações contínuas não serão ativadas em produção agora para evitar consumo desnecessário de cota, mas o código já foi desenhado pensando em suportá-las facilmente.

---

## 1. Ingestão Incremental Agendada (A cada X dias)

Hoje o `ingest_pncp.py` faz uma carga histórica completa (*Backfill*) desde `2024-01-01` conforme definido no `config.yaml`. A idempotência já protege a camada de classificação (`numero_controle_pncp`) e a subida para o BigQuery (`_row_hash`), evitando duplicações.

Porém, se fôssemos colocar esse pipeline para rodar automaticamente a cada 3 dias (por exemplo, via GitHub Actions), não faria sentido bater na API do PNCP pedindo dados desde 2024 toda vez. Existem duas abordagens simples que se encaixam direto na estrutura atual:

### Abordagem A: Janela Deslizante (*Sliding Window*) no `config.yaml`
Adicionar um parâmetro `lookback_days: 7` no `config.yaml`. Quando ativo, o `ingest_pncp.py` ignora o `start_date` fixo e busca apenas os últimos 7 dias (`hoje - 7 dias` até `hoje`).
- **Por que 7 dias se o pipeline roda a cada 3?** Essa sobreposição de dias funciona como margem de segurança: se a API do governo cair num dia, a execução seguinte recupera os dados perdidos. E como o `load_to_bigquery.py` e o `run_classification.py` são idempotentes, os dias repetidos são filtrados automaticamente sem custo extra.

### Abordagem B: Marca D'Água (*High Watermark*) via BigQuery
Antes de iniciar o download na API, o script faz uma consulta rápida no BigQuery:
```sql
SELECT MAX(data_publicacao) FROM `pncp-project.stg_pncp.stg_contratacoes`
```
- Se a tabela ainda não existir (primeira execução), ele roda o histórico completo desde `2024-01-01`.
- Se já existir, ele usa a última data encontrada (com alguns dias de folga para capturar eventuais atualizações recentes) como ponto de partida da busca.

---

## 2. Extração de Itens Homologados Apenas para Contratações de TIC

O endpoint `/v1/contratacoes/publicacao` traz o resumo do edital e o valor global, mas não lista os itens individuais comprados (ex: marca/modelo do notebook, quantidade exata de licenças e valor unitário).
Na API do PNCP, os itens ficam na sub-rota `/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens`, o que exige 1 requisição HTTP por licitação.

- **Problema na base bruta:** Fazer 5.176 requisições individuais para todas as compras do município seria lento e pesado.
- **Solução habilitada pela classificação de IA:** Como agora temos a tabela `bronze_classificacao_tic_ia` identificando exatamente quais processos são de fato TIC, um script futuro pode filtrar apenas os IDs onde `is_tic = True` (uma fração pequena da base total) e buscar o detalhamento de itens e fornecedores vencedores somente para essas contratações.
