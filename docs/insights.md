# Principais Insights — Compras Públicas de TIC em Santos/SP (2024–2026)

Este documento reúne a leitura analítica sobre os resultados da camada Gold (`marts_pncp.fct_contratacoes`), consolidados em [`dbt_pncp/analyses/resultados_analises.md`](../dbt_pncp/analyses/resultados_analises.md). O objetivo é ir além das tabelas e responder o **"e daí?"** dos números, cruzando os achados do banco com o contexto real de Santos/SP, plataformas de inteligência de mercado e diretrizes de órgãos de controle.

---

## Eixo 0 — Visão Geral: Volume vs. Complexidade

Considerando os **247 processos de TIC válidos** (`Homologada` + `Em Andamento`, deixando de fora os cancelados e os encerrados sem homologação), o recorte soma aproximadamente **R$ 260,29 milhões estimados** e **R$ 143,31 milhões homologados**, com ticket médio de **R$ 604,67 mil** entre os processos já homologados.

Olhando a distribuição entre as 4 categorias de TIC, fica clara uma inversão entre esforço operacional e peso financeiro:

- **Hardware e Equipamentos** responde por **54,25% dos processos** (134 de 247), mas representa apenas **11,23% do valor homologado** (R$ 16,10 milhões).
- **Serviços de TI** representa apenas **14,17% dos processos** (35 editais), mas concentra **43,24% de todo o orçamento homologado** (R$ 61,97 milhões).
- **Redes, Cloud e Segurança** (50 processos; **20,24%** em volume e **22,78%** do valor = R$ 32,65 milhões) e **Software e Licenciamento** (28 processos; **11,34%** em volume e **22,74%** do valor = R$ 32,59 milhões) dividem o restante do orçamento praticamente meio a meio.

**Leitura de negócio e hipótese no contexto de Santos:**
- **Hardware** é a compra mais rotineira e pulverizada do dia a dia (aquisição de desktops, monitores, fones de ouvido para escolas da SEDUC, periféricos do IPREV e suprimentos), o que explica abrir mais da metade dos editais para um valor agregado menor.
- Já **Serviços de TI**, **Redes/Segurança** e **Software**, embora tenham menos processos abertos, refletem projetos mais caros e complexos previstos nas diretrizes de tecnologia da [Prefeitura de Santos (Licita Santos / DETIC)](https://www.santos.sp.gov.br/licitasantos/) e da [Autoridade Portuária de Santos (APS / Porto de Santos)](https://www.portodesantos.com.br/): contratos plurianuais (36 a 60 meses) de sustentação do Centro de Controle Operacional (CCO), monitoramento CFTV, evolução do *Santos Digital*, sistemas de gestão/BI e operação de infraestrutura crítica portuária.

---

## Eixo 1 — Economicidade, Deságio e Qualidade da Orçamentação

> **O que é o deságio?** É a diferença (em R$ ou %) entre o valor estimado inicialmente pelo órgão público no edital e o valor final homologado após a disputa de lances.

### 1.1 Comparativo com Fontes Externas (BreveIA, Painel de Compras, TCU e Enap)
Ao comparar os nossos resultados com plataformas de mercado e estudos oficiais, encontramos números que parecem distantes à primeira vista, mas que se explicam pela metodologia de cálculo:

- **Agregadores Nacionais de Mercado ([BreveIA](https://www.breveia.com.br/mercado/tecnologia/), [Effecti](https://www.effecti.com.br/blog/) e [Lance Fácil](https://www.lancefacil.com/)):** Levantamentos que consolidam todas as contratações homologadas de Tecnologia no [PNCP](https://www.gov.br/pncp/pt-br) apontam um **deságio médio geral de 7,0%** no país.
- **Estudos de Pregão Eletrônico ([TCU](https://portal.tcu.gov.br/), [Enap](https://repositorio.enap.gov.br/) e [Painel de Compras do Governo Federal](https://www.gov.br/compras/pt-br/acesso-a-informacao/painel-de-compras)):** Análises focadas exclusivamente em licitações competitivas (pregões eletrônicos) apontam deságios históricos na faixa de **15% a 30%**, frequentemente **superando 30%** em bens e serviços padronizados de TI onde há disputa automatizada de lances.
- **Cenário observado em Santos (`Licitação Competitiva`):**
  - **Redes, Cloud e Segurança:** `41,98%` (31 processos homologados)
  - **Software e Licenciamento:** `37,70%` (12 processos homologados)
  - **Não-TIC (referência geral do município):** `33,86%` (2.604 processos homologados)
  - **Hardware e Equipamentos:** `32,17%` (82 processos homologados)
  - **Serviços de TI:** `30,85%` (28 processos homologados)

**Por que a nossa média fica entre 30,85% e 41,98% enquanto agregadores gerais citam 7%?**
1. **Filtro estrito de disputa:** Na nossa consulta (`desagio_tic_e_nao_tic.sql`), filtramos apenas **`Licitação Competitiva` (Pregão e Concorrência)** com orçamento aberto (`valor_total_estimado > 0`). Agregadores que tiram a média sobre *toda* a base homologada do PNCP incluem milhares de **Dispensas e Inexigibilidades** no denominador — onde não há disputa de lances e o deságio é `0%`, puxando a média nacional para perto de `7%`.
2. **Atratividade regional:** Santos concentra compradores de grande porte no eixo da Baixada Santista (Prefeitura, Porto de Santos/APS, unidades estaduais de Saúde e Segurança), utilizando plataformas eletrônicas integradas ao PNCP com forte presença de fornecedores e robôs de lances.

### 1.2 Anomalias de Extremos (`-542%` vs. `+93%`) e o "Paradoxo do Deságio"
- **Zero sobrepreço em TIC vs. outlier negativo em Não-TIC:** Nas licitações competitivas de TIC, o deságio mínimo foi **`0,00%`** (nenhum processo fechou acima do estimado). Já em **Não-TIC**, o mínimo chegou a **`-542,01%`** (valor homologado mais de 6x acima do estimado). Na base do PNCP, extremos negativos assim costumam decorrer de **erro de digitação ou divergência cadastral** (estimativa preenchida pelo valor unitário do item e homologação lançada pelo valor global do lote/contrato).
- **Superestimativa em Redes, Cloud e Telecom:** Na outra ponta, descontos entre **70% e 93,34%** em TIC (e até `99,98%` em Não-TIC) ilustram o que auditorias do [TCU](https://portal.tcu.gov.br/) chamam de **"Paradoxo do Deságio"**: descontos próximos de 80%–90% não refletem apenas concorrência feroz, mas principalmente **orçamentos estimados inflados na fase interna da licitação**.
- Nos dados de Santos, isso fica evidente em **Redes, Cloud e Segurança**, onde contratos *on-demand* e serviços de telecomunicações tornam a cesta de preços mais difícil de estimar:
  - **Prefeitura de Santos (`58200015000183-1-000526/2025`):** contratação de 3 links dedicados de conectividade IP redundantes por 5 anos para o datacenter do Paço Municipal — estimado em **R$ 3,76 milhões** e homologado por **R$ 889,56 mil** (**76,36% de deságio**, quase R$ 2,87M de diferença em um único edital).
  - **Câmara Municipal de Santos (`49203409000102-1-000038/2026`):** telefonia fixa comutada (STFC) com Tronco SIP — estimado em **R$ 120,15 mil** e homologado por **R$ 8,00 mil** (**93,34% de deságio**).
  - **Porto de Santos / CODESP (`44837524000107-1-000033/2026`):** sistema de radiocomunicação por 36 meses para a Autoridade Portuária — estimado em **R$ 9,51 milhões** e homologado por **R$ 3,22 milhões** (**66,13% de deságio**).

### 1.3 Evolução da Economia (2024–2026)
Desde 2024, com a aplicação da Nova Lei de Licitações ([Lei nº 14.133/2021](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm)), a economia bruta acumulada em TIC no município somou **R$ 81,49 milhões** (**R$ 49,89 milhões apenas em 2026**, R$ 29,55 milhões em 2025 e R$ 2,05 milhões em 2024).
- O **deságio médio simples** (onde cada contrato tem o mesmo peso) manteve-se entre **24,06%** (2024), **34,40%** (2025) e **27,40%** (2026).
- Já o **deságio médio ponderado** subiu de **17,43% em 2024 para 40,22% em 2026**, puxado pelos grandes contratos de infraestrutura e serviços plurianuais.

### 1.4 Funil de Desfecho: Quase R$ 90 milhões que não saíram do papel
Olhando todos os **353 processos de TIC** da base:
- **67,14% (237 processos)** finalizaram **Homologados** (R$ 224,77 milhões estimados).
- **28,05% (99 processos)** ficaram **Encerrados sem Homologação**, somando **R$ 89,32 milhões** em valor estimado que não avançaram (além de 7 processos cancelados/revogados somando R$ 466,79 mil e 10 ainda em andamento).

Ter quase **R$ 90 milhões estimados** parados em processos sem homologação conversa diretamente com os alertas do [TCESP (Tribunal de Contas do Estado de São Paulo)](https://www.tce.sp.gov.br/): editais de TI com pesquisa de preços mal calibrada (gerando licitações desertas ou fracassadas) ou com exigências técnicas excessivamente restritivas acabam travando a contratação e gerando retrabalho para a administração.

---

## Eixo 2 — Competitividade, Amparos Legais e Risco de Fracionamento

- **O Pregão domina o orçamento, mas a Dispensa pulveriza os processos:** O Pregão Eletrônico concentra **99,84%** do valor homologado em Redes/Cloud, **99,00%** em Serviços de TI, **98,15%** em Hardware e **79,25%** em Software (onde houve também 1 Concorrência Eletrônica de R$ 6,00 milhões = `18,41%`). Em quantidade de processos, porém, a **Dispensa** ainda aparece bastante em **Hardware** (46 dispensas vs. 82 pregões) e **Software** (11 dispensas vs. 11 pregões).
- **Amparos legais nas 84 contratações diretas homologadas:**
  - **72 processos (85,7%)** são Dispensas por baixo valor (`Lei 14.133/2021, Art. 75, II`), somando **R$ 424,04 mil**.
  - O maior volume financeiro em contratação direta veio de **1 Dispensa emergencial** (`Art. 75, VIII`) de **R$ 532,80 mil** e **4 Dispensas para contratação de órgão/entidade pública de TI** (`Art. 75, IX`, R$ 423,42 mil).
  - Apenas **5 processos** usaram **Inexigibilidade por fornecedor exclusivo** (`Art. 74, I`, R$ 142,73 mil) — como licenças específicas ou links MPLS/SD-WAN da Marinha —, indicando baixo grau de *lock-in* via contratação direta.
- **Radar de dispensas repetidas:** A unidade `MSP-PREFEITURA MUNICIPAL DE SANTOS` realizou **10 dispensas de Hardware em 2025** (R$ 27,26 mil homologados) e **5 em 2026** (R$ 56,17 mil homologados). Os valores somados respeitam os limites legais, mas evidenciam compras picadas recorrentes que poderiam ser unificadas.

---

## Eixo 3 — Governança, Órgãos Compradores e Ganho de Escala

- **Prefeitura de Santos (Municipal) vs. Porto de Santos (Federal):** Como o filtro do PNCP é o código IBGE de Santos (`3548500`), a base captura órgãos municipais, estaduais e federais sediados na cidade. Consolidando as contratações pelo órgão comprador (`orgao_razao_social`), dois grandes atores concentram **89,5%** de todo o gasto homologado de TIC da cidade (`R$ 128,26M` de `R$ 143,31M`), mas com perfis opostos:
  - O **Município de Santos** lidera em valor total e em volume operacional: **R$ 65,39 milhões homologados** (`45,6%` do total) pulverizados em **91 processos** distribuídos por **6 unidades compradoras** (incluindo `MSP-PREFEITURA MUNICIPAL DE SANTOS`, `Prefeitura Municipal de Santos`, `SECRETARIA DE GESTAO` e `SECRETARIA MUNICIPAL DE SAUDE`).
  - A **Companhia Docas do Estado de São Paulo ([APS / Porto de Santos](https://www.portodesantos.com.br/))**, esfera Federal, vem logo atrás com **R$ 62,87 milhões homologados** (`43,9%` do total) concentrados em apenas **11 processos** (1 unidade). Isso reflete o ciclo recente (2025–2026) de grandes projetos estruturantes de modernização portuária (suporte operacional de TIC, radiocomunicação, segurança cibernética e monitoramento de tráfego aquaviário VTMIS).
  - Na sequência aparecem a **Câmara Municipal de Santos** (**R$ 5,74 milhões** em 23 processos / 2 unidades), a **Secretaria de Estado da Saúde** (**R$ 4,35 milhões** em 35 processos / 2 unidades) e a **Secretaria da Segurança Pública** (**R$ 1,83 milhão** em 37 processos / 4 unidades).
  - **Nota de qualidade de dados ([AUDESP Fase V / TCESP](https://www.tce.sp.gov.br/audesp) e PNCP):** Sem consolidar por `orgao_razao_social`, o PNCP fragmenta o mesmo órgão em diferentes grafias de unidade compradora (ex.: `CAMARA MUNICIPAL DE SANTOS` vs. `CÂMARA MUNICIPAL DE SANTOS - SP`, e 6 variações de unidades para a Prefeitura), o que antes fazia parecer que a CODESP gastava o dobro do Município.
- **Porte da contratação vs. Deságio:**
  - Na média percentual simples, compras de **Médio Porte** (`36,38%`, 43 processos) e **Pequeno Porte** (`35,21%`, 75 processos) tiveram descontos médios superiores às de **Grande Porte** (`29,99%`, 35 processos).
  - Porém, em volume financeiro economizado, os **35 processos de Grande Porte (acima de R$ 500 mil)** geraram **R$ 77,78 milhões de economia** — respondendo por **95,7%** de toda a economia absoluta das licitações competitivas.

---

## Eixo 4 — Sazonalidade, Janela de Propostas e Registro de Preços (SRP)

- **Sem concentração rígida no fim do ano (Q4):** Ao contrário do senso comum de que o setor público concentra as compras no último trimestre para queimar orçamento, os gastos trimestrais em Santos oscilaram conforme a abertura de grandes editais: em 2024 o pico homologado foi no Q4 (R$ 5,64M), mas em 2025 ocorreu no **Q2** (R$ 26,31M) e em 2026 logo no **1º trimestre** (R$ 57,26M). Os trimestres Q3 e Q4 de 2026 acumulam mais de R$ 56 milhões estimados cada, mas ainda com menor valor homologado por reunirem processos mais recentes.
- **Prazos de proposta e oportunidade clara em Atas (SRP):**
  - A janela média de propostas acompanha a complexidade legal: **6,6 dias** na Dispensa, **17,0 dias** no Pregão Eletrônico e **41,3 dias** na Concorrência Eletrônica.
  - Em contrapartida, a adesão ao **Sistema de Registro de Preços (SRP)** é baixa: apenas **7,89%** dos Pregões Eletrônicos (18 de 228) e **0,86%** das Dispensas (1 de 116) utilizam SRP.

---

## Hipóteses de Melhoria e Ideias Práticas

A partir dos dados analisados, levantamos **4 propostas práticas** para ganho de eficiência nas compras públicas de TIC e evolução da própria análise:

1. **Calibração da Cesta de Preços em Categorias Não Padronizadas (Redução de Outliers e Fracassos):**
   - **Problema nos dados:** Deságios médios de `41,98%` em Redes/Cloud (com picos de `76%` a `93%`) e `28,05%` de processos encerrados sem homologação (~R$ 89,32M estimados travados).
   - **Ideia de melhoria:** Em serviços *on-demand*, cloud e telecomunicações, substituir cotações diretas isoladas com fornecedores (que costumam inflar o preço de referência) por cestas baseadas em **preços já homologados no próprio PNCP** e no [Painel de Preços / Compras.gov.br](https://www.gov.br/compras/pt-br/acesso-a-informacao/painel-de-compras), seguindo as diretrizes da [IN SEGES/ME nº 65/2021](https://www.gov.br/compras/pt-br/acesso-a-informacao/legislacao/instrucoes-normativas/instrucao-normativa-seges-me-no-65-de-7-de-julho-de-2021). Isso aproxima o valor estimado do preço real de mercado, reduzindo tanto a reserva orçamentária ociosa quanto o índice de licitações fracassadas.

2. **Centralização de Compras de Hardware via Atas de Registro de Preços (SRP):**
   - **Problema nos dados:** Hardware consome **54,25%** do esforço de abertura de editais para representar apenas **11,23%** do orçamento, somando dezenas de Dispensas avulsas na mesma unidade compradora enquanto apenas **7,89%** dos pregões usam SRP.
   - **Ideia de melhoria:** Instituir Atas de Registro de Preços anuais padronizadas pelo departamento central de TI (como o DETIC na Prefeitura) para itens recorrentes (desktops, monitores, headsets, cabos e adaptadores), liberando a equipe de licitações para focar nos contratos complexos de Serviços e Software (que concentram quase 66% do orçamento).

3. **Saneamento Cadastral e Validação de Unidades no Envio ao PNCP:**
   - **Problema nos dados:** O mesmo órgão comprador aparece fragmentado em múltiplas unidades com grafias distintas, além de itens de TI misturados a compras de copa/papelaria em dispensas e outliers negativos (`-542%` em Não-TIC) por inversão entre preço unitário e global.
   - **Ideia de melhoria:** Padronizar o cadastro de unidades gestoras na integração dos sistemas locais com o PNCP e criar travas de validação entre o valor unitário estimado e o valor global homologado.

4. **Expansão Analítica para o Grão de `/itens` e `/resultados` (Próximo Passo do Projeto):**
   - **Limite atual:** O endpoint `/v1/contratacoes/publicacao` analisa o cabeçalho do edital, o que responde perguntas macro de governança, orçamento e modalidade, mas não mostra **quem venceu** nem o **preço unitário por item**.
   - **Ideia de evolução (mapeada em [`future_features.md`](future_features.md)):** Ingerir os endpoints de itens e resultados dos 353 processos de TIC para auditar concentração de mercado (quais CNPJs mais vencem em Santos) e comparar o preço unitário pago por equipamento.

---

## Fontes e Referências Consultadas

- **Dados Oficiais e Legislação:**
  - [PNCP — Portal Nacional de Contratações Públicas (API de Dados Abertos)](https://www.gov.br/pncp/pt-br)
  - [Lei Federal nº 14.133/2021 (Nova Lei de Licitações e Contratos)](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm)
  - [IN SEGES/ME nº 65/2021 (Pesquisa de Preços nas Contratações Públicas)](https://www.gov.br/compras/pt-br/acesso-a-informacao/legislacao/instrucoes-normativas/instrucao-normativa-seges-me-no-65-de-7-de-julho-de-2021)
- **Contexto Local (Santos/SP):**
  - [Prefeitura Municipal de Santos — Portal Licita Santos e Transparência](https://www.santos.sp.gov.br/licitasantos/)
  - [Porto de Santos (APS — Autoridade Portuária de Santos) — Licitações e Investimentos em TIC](https://www.portodesantos.com.br/)
- **Controle Externo e Literatura Técnica:**
  - [TCU — Tribunal de Contas da União (Publicações e Jurisprudência sobre Contratações de TI e Deságio)](https://portal.tcu.gov.br/)
  - [TCESP — Tribunal de Contas do Estado de São Paulo (AUDESP Fase V e Boletins de Jurisprudência)](https://www.tce.sp.gov.br/audesp)
  - [Enap — Repositório Institucional (Estudos sobre Economicidade e Pregão Eletrônico)](https://repositorio.enap.gov.br/)
  - [Painel de Compras do Governo Federal (MGI / Compras.gov.br)](https://www.gov.br/compras/pt-br/acesso-a-informacao/painel-de-compras)
- **Plataformas de Inteligência de Mercado B2G:**
  - [BreveIA — Panorama do Mercado de Tecnologia no PNCP](https://www.breveia.com.br/mercado/tecnologia/)
  - [Effecti — Inteligência em Licitações e Pregões Eletrônicos](https://www.effecti.com.br/blog/)
  - [Lance Fácil — Automação e Dados de Licitações Públicas](https://www.lancefacil.com/)
