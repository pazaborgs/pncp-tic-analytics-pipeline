# Decisões de Análise e Feature Engineering — Camada Gold (`marts_pncp.fct_contratacoes`)

## Panorama da Extração e Escopo

- **Endpoint:** Contratações por Data de Publicação (`/v1/contratacoes/publicacao`)
- **Município:** Santos/SP (`codigoMunicipioIbge = 3548500`)
  - Extrair todas as contratações do município e classificar o recorte de TIC sobre `objetoCompra` (classificação semântica em lote via LLM com validação estatística estratificada).
- **Modalidades:** Pregão Eletrônico (6), Dispensa de Licitação (8), Inexigibilidade (9), Concorrência Eletrônica (4) e Credenciamento (12).
- **Janela Temporal:** 01/01/2024 – Hoje (divisão em janelas semestrais).

> **Decisão Arquitetural da Camada Gold:**
> - **Tabela Única (`fct_contratacoes`):** Manter apenas uma tabela Fato consolidada (1 linha por contratação) com a flag booleana `is_tic` (`TRUE`/`FALSE`) e `categoria_tic`. Isso permite tanto filtrar exclusivamente TIC (`WHERE is_tic = TRUE`) quanto comparar o comportamento de **TIC vs. Não-TIC** (`GROUP BY is_tic`).
> - **Granularidade:** As colunas de *Feature Engineering* são calculadas linha a linha na Gold sem agregar/esmagar por ano na tabela base, preservando a capacidade de aplicar filtros dinâmicos (ano, esfera, órgão, modalidade) no BI/Dashboard.

---

## 0. Visão Executiva e KPIs de Topo

### Perguntas Norteadoras
- **0.1 — Termômetro Geral (TIC vs. Não-TIC):** Qual o volume de processos, total estimado, total homologado e ticket médio das compras de TIC em Santos (desconsiderando canceladas)? (`analyses/eixo_0_visao_geral/kpis_gerais.sql`)
- **0.2 — Raio-X das Categorias de TIC:** Como o volume de processos e o valor homologado se distribuem entre as 4 categorias de TIC e qual o *share %* de cada uma? (`analyses/eixo_0_visao_geral/percentual_categoria_tic.sql`)

---

## 1. Economicidade e Qualidade da Orçamentação (Deságio)

### Perguntas Norteadoras e Consultas
- **1.1 — Evolução Anual da Economia:** Qual a economia total (R$ e % médio simples vs. ponderado) gerada entre `valor_total_estimado` e `valor_total_homologado` em TIC por ano? (`analyses/eixo_1_economicidade/economia_anual_tic.sql`)
- **1.2 — Comparativo de Deságio:** O deságio percentual em TIC nas modalidades competitivas é maior ou menor que nas demais compras (`Não-TIC`) do município? (`analyses/eixo_1_economicidade/desagio_tic_e_nao_tic.sql`)
- **1.3 — Funil de Desfecho:** Dos processos de TIC abertos desde 2024, quantos chegaram à homologação e quanto orçamento estimado ficou travado em compras canceladas ou encerradas sem homologação? (`analyses/eixo_1_economicidade/funil_status_tic.sql`)
- **1.4 — Auditoria de Extremos (*Outliers*):** Quais contratações apresentaram distorções extremas de estimativa (`desagio_absoluto < 0` ou `desagio_percentual > 70`) no geral e por órgão comprador? (`analyses/eixo_1_economicidade/outliers_orcamentacao_tic.sql` e `maior_extremo_por_orgao.sql`)

### Features e Regras de Cálculo na Gold
1. **`desagio_absoluto` (Economia em R$):** `valor_total_estimado - valor_total_homologado` (calculado apenas quando ambos são `> 0`).
2. **`desagio_percentual`:** `ROUND(SAFE_DIVIDE(valor_total_estimado - valor_total_homologado, valor_total_estimado) * 100, 2)`.
3. **`status_processo`:**
   - `'Cancelada (Revogada/Anulada/Suspensa)'`: quando `situacao_compra_id IN (2, 3, 4)`.
   - `'Homologada'`: quando `valor_total_homologado > 0`.
   - `'Em Andamento'`: quando `valor_total_homologado IS NULL` e `dt_encerramento_proposta >= CURRENT_TIMESTAMP()`.
   - `'Encerrada sem Homologação'`: quando `valor_total_homologado IS NULL` e o prazo de propostas já encerrou.

---

## 2. Modalidades, Competitividade e Risco de *Lock-in* / Fracionamento

### Perguntas Norteadoras e Consultas
- **2.1 — Competição vs. Contratação Direta:** Qual a proporção (quantidade e valor R$) entre Pregão/Concorrência vs. Dispensa e Inexigibilidade dentro de cada categoria de TIC? (`analyses/eixo_2_competitividade/competitividade_por_categoria.sql`)
- **2.2 — Top Amparos Legais:** Quais artigos da lei justificam as contratações sem licitação de TIC? (`analyses/eixo_2_competitividade/amparos_legais_direta.sql`)
- **2.3 — Radar de Fracionamento:** Quais unidades compradoras realizaram 3 ou mais Dispensas (`modalidade_id = 8`) para a mesma categoria de TIC no mesmo exercício? (`analyses/eixo_2_competitividade/radar_fracionamento_dispensas.sql`)

### Features e Regras de Cálculo na Gold
1. **`grupo_competitividade`:**
   - `'Licitação Competitiva'`: Pregão Eletrônico (`6`), Concorrência Eletrônica (`4`).
   - `'Contratação Direta'`: Dispensa de Licitação (`8`), Inexigibilidade (`9`).
   - `'Procedimento Auxiliar'`: Credenciamento (`12`).
2. **`categoria_tic` e `is_tic`:** Classificação semântica vinda da tabela `bronze_classificacao_tic_ia` via `LEFT JOIN` na Silver (`stg_contratacoes`):
   - `'Software e Licenciamento'`, `'Hardware e Equipamentos'`, `'Redes, Cloud e Segurança'`, `'Serviços de TI'` e `'Não-TIC'`.

---

## 3. Governança e Centralidade de Compras

### Perguntas Norteadoras e Consultas
- **3.1 — Quem compra TIC em Santos:** Como os gastos se dividem entre as esferas (Municipal, Estadual e Federal) e quais as 10 unidades compradoras que mais concentram recursos? (`analyses/eixo_3_governanca/top_unidades_compradoras.sql`)
- **3.2 — Ganho de Escala:** Compras de grande porte obtêm maior deságio percentual que compras pequenas/médias nas licitações competitivas de TIC? (`analyses/eixo_3_governanca/escala_porte_vs_desagio.sql`)

### Features e Regras de Cálculo na Gold
1. **`orgao_esfera_nome`:** Tradução dos códigos (`'M'` $\rightarrow$ `'Municipal'`, `'E'` $\rightarrow$ `'Estadual'`, `'F'` $\rightarrow$ `'Federal'`).
2. **`porte_contratacao` (Faixas pelo `valor_total_estimado`):**
   - `'Pequeno Porte (Até R$ 60 mil)'`
   - `'Médio Porte (R$ 60 mil a R$ 500 mil)'`
   - `'Grande Porte (Acima de R$ 500 mil)'`

---

## 4. Dinâmica Temporal, Sazonalidade e Registro de Preços (SRP)

### Perguntas Norteadoras e Consultas
- **4.1 — Sazonalidade:** Como as publicações e valores de TIC se distribuem ao longo dos trimestres (há concentração no fim do ano)? (`analyses/eixo_4_sazonalidade/sazonalidade_trimestral_tic.sql`)
- **4.2 — Janela de Propostas e Atas (SRP):** Qual o prazo médio concedido ao mercado por modalidade e qual a taxa de adesão ao Sistema de Registro de Preços (`is_srp`)? (`analyses/eixo_4_sazonalidade/janela_propostas_e_srp.sql`)

### Features e Regras de Cálculo na Gold
1. **Atributos de Calendário e Sazonalidade:** `ano_publicacao`, `mes_publicacao`, `trimestre_publicacao` e `is_fim_de_ano` (`trimestre_publicacao = 4`).
2. **`dias_janela_proposta`:** `TIMESTAMP_DIFF(dt_encerramento_proposta, dt_abertura_proposta, DAY)`.
3. **Indicador de SRP (`is_srp`):** Booleano indicando uso de Ata de Registro de Preços.
