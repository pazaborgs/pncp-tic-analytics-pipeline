# Contexto do Projeto e Escopo Analítico — PNCP (Santos/SP)

O PNCP é a sigla para Portal Nacional de Contratações Públicas.

Trata-se do site oficial do governo brasileiro criado pela Nova Lei de Licitações e Contratos Administrativos (Lei nº 14.133/2021) com o objetivo de centralizar e dar transparência a todas as compras e contratações públicas do país.

---

## Ciclo de Compras — Lei nº 14.133/2021

PCA → Processo de contratação → Seleção do fornecedor → ARP (quando aplicável) → Contrato → Execução contratual.

### 1. Planejamento — PCA (Plano de Contratações Anual)

Elaborado no meio do ano anterior como um orçamento de intenções: reúne tudo o que os órgãos pretendem contratar no exercício seguinte (incluindo o PDTIC, no caso de tecnologia).

### 2. Seleção do Fornecedor — Contratações (Compras, Editais e Avisos)

Os órgãos publicam suas demandas de aquisição através das modalidades previstas em lei. As principais analisadas neste projeto são:

- **Pregão Eletrônico (código 6):** Regra geral para bens e serviços comuns, com disputa aberta de lances.
- **Dispensa de Licitação (código 8):** Contratações diretas por baixo valor ou situações emergenciais.
- **Inexigibilidade (código 9):** Quando há inviabilidade de competição (fornecedor exclusivo ou serviço técnico especializado).

Este é o endpoint central da extração (`/v1/contratacoes/publicacao`), por concentrar os metadados financeiros, operacionais e jurídicos mais completos de cada processo.

### 3. Atas de Registro de Preços (ARP)

Em vez de o órgão comprar 1.000 computadores de uma vez, ele faz um Pregão com Sistema de Registro de Preços (`srp: true`). O vencedor assina uma Ata comprometendo-se a manter o preço por 1 ano.
- Isso não significa que a Prefeitura seja obrigada a comprar todos os 1.000 computadores.
- Outros órgãos podem aderir à ata como participantes não originais, desde que respeitem os requisitos legais para adesão.

### 4. Contratos

Depois que a licitação acaba (ou a ata é acionada), assina-se o Contrato com vigência, CNPJ do fornecedor contratado, valor global e aditivos. Em TIC, contratos de serviços contínuos (cloud, link de dados, fábrica de software, suporte) duram anos.

---

## Teoria do Domínio — O que estamos extraindo?

O endpoint `/v1/contratacoes/publicacao` retorna uma fotografia de cada **processo de contratação pública** divulgado no Portal Nacional de Contratações Públicas. Abaixo está o dicionário conceitual de cada grupo de campos do JSON e como interpretá-los em análises.

### 1. Identificadores e Chaves de Negócio

Uma confusão comum no setor público é misturar o número do processo administrativo, o número do edital e a chave do PNCP.

| Campo no JSON | Significado na Administração Pública | Papel na Engenharia de Dados (dbt / SQL) |
| :--- | :--- | :--- |
| **`numeroControlePNCP`** | Identificador nacional único gerado pelo PNCP no formato `CNPJ-1-SEQUENCIAL/ANO` (ex.: `46374500000194-1-008187/2025`). | **Chave Primária Natural (PK)** da tabela fato de contratações. |
| **`sequencialCompra`** e **`anoCompra`** | Número sequencial interno que o PNCP atribui para aquele CNPJ dentro daquele ano. | Compõem a URL de sub-rotas da API (como consulta de itens e arquivos: `/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens`). |
| **`numeroCompra`** | Número do edital ou aviso na numeração local do órgão (ex.: Pregão nº `90388/2025` ou `075/2023`). | Útil para gestores humanos localizarem o edital, mas **não é único** (órgãos diferentes usam o mesmo número). |
| **`processo`** | Número do Processo Administrativo eletrônico interno (ex.: SEI, Processo Digital da Prefeitura). | Rastreabilidade jurídica/auditoria em caso de investigação de uma compra específica. |

### 2. Hierarquia Institucional: Órgão vs. Unidade Compradora

Quando filtramos `codigoMunicipioIbge = 3548500` (Santos/SP), a API filtra pelo **endereço físico da Unidade Compradora (`unidadeOrgao`)**, e não apenas pela Prefeitura. Por isso o JSON separa a instituição em dois objetos aninhados:

#### A. `orgaoEntidade` (A Pessoa Jurídica / CNPJ Principal)
Representa a entidade máxima detentora do CNPJ:
* **`cnpj` e `razaoSocial`:** Ex.: *Município de Santos*, *Câmara Municipal de Santos*, *Secretaria de Estado da Saúde (SP)*, *Universidade Federal de São Paulo (UNIFESP)*.
* **`esferaId` (Esfera Governamental):**
  * **`"M"` (Municipal):** Prefeitura de Santos, Câmara Municipal, autarquias e fundações municipais.
  * **`"E"` (Estadual):** Órgãos do Governo do Estado de SP sediados em Santos (ex.: Hospital Guilherme Álvaro, FATEC, Polícia Militar).
  * **`"F"` (Federal):** Órgãos da União sediados em Santos (ex.: Autoridade Portuária de Santos, Alfândega da Receita Federal, Marinha, UNIFESP Baixada Santista).
* **`poderId` (Poder da República):**
  * **`"E"` (Executivo):** Prefeituras, Governo do Estado, Ministérios.
  * **`"L"` (Legislativo):** Câmaras Municipais, Assembleias, Tribunais de Contas.
  * **`"J"` (Judiciário):** Tribunais de Justiça, Justiça Federal/Trabalhista.
  * **`"N"` (Não se aplica / Outros):** Algumas entidades ou cadastros legados.

#### B. `unidadeOrgao` (A Unidade Administrativa / UASG que executou a compra)
Dentro de um mesmo CNPJ (como a Prefeitura de Santos), várias secretarias ou departamentos podem operar licitações:
* **`codigoUnidade` e `nomeUnidade`:** Identificam a secretaria ou departamento comprador.
* **`codigoIbge`, `municipioNome`, `ufSigla`:** A localização geográfica daquela unidade (`3548500` - Santos/SP).

#### C. `orgaoSubRogado` e `unidadeSubRogada`
* Na maioria dos casos vêm como `null`. Só são preenchidos quando uma unidade transfere formalmente a responsabilidade daquela compra para outra unidade (sub-rogação administrativa).

### 3. Classificação Jurídica, Modalidades e Competitividade

Estes campos explicam **como** o órgão decidiu contratar e qual o nível de competição aplicado:

* **`modalidadeId` e `modalidadeNome`:**
  * `6` (*Pregão - Eletrônico*): Modalidade competitiva padrão para bens e serviços comuns (incluindo TIC).
  * `8` (*Dispensa de Licitação*): Contratação direta (geralmente por baixo valor — art. 75, I e II — ou emergência — art. 75, VIII).
  * `9` (*Inexigibilidade*): Contratação direta quando há inviabilidade de competição (fornecedor exclusivo, licenças de software proprietárias sem equivalentes).
  * `4` (*Concorrência - Eletrônica*): Obras, serviços especiais de engenharia ou bens/serviços especiais de grande complexidade.
  * `12` (*Credenciamento*): Procedimento auxiliar onde todos os interessados que cumprem os requisitos são contratados pelo mesmo preço tabelado.
* **`modoDisputaId` e `modoDisputaNome`:**
  * Define a dinâmica de lances dos fornecedores: *Aberto* (lances públicos sucessivos), *Aberto-Fechado* (etapa aberta seguida de lance final sigiloso — muito eficaz para forçar descontos reais), *Fechado* ou *Não se aplica* (em dispensas sem disputa/inexigibilidades).
* **`tipoInstrumentoConvocatorioCodigo` e `tipoInstrumentoConvocatorioNome`:**
  * *Edital* (em licitações como Pregão e Concorrência), *Aviso de Contratação Direta* (em Dispensas Eletrônicas com disputa de lances) ou *Ato que autoriza a Contratação Direta* (em Dispensas sem disputa e Inexigibilidades).
* **`amparoLegal` (`codigo`, `nome`, `descricao`):**
  * Traz exatamente o artigo e inciso da lei (ex.: `Lei 14.133/2021, Art. 28, I` ou `Art. 75, II`). Em auditoria de TIC, agrupar por `amparoLegal.nome` revela imediatamente se o órgão usa dispensa por valor baixo ou por emergência.

### 4. Valores Financeiros, SRP e Situação da Compra

* **`valorTotalEstimado`:** O valor de referência orçado pela administração antes de abrir a disputa (teto ou preço estimado).
* **`valorTotalHomologado`:** O valor final fechado após os lances e a aprovação (homologação) da autoridade competente.
  * **Por que `valorTotalHomologado` às vezes vem `null`?**
    1. A licitação **ainda está em andamento** (fase de propostas, lances ou análise de habilitação/recursos).
    2. A licitação foi **deserta** (ninguém apareceu), **fracassada** (todos foram desclassificados), **suspensa**, **revogada** ou **anulada**.
    3. O sistema de origem do município publicou o edital no PNCP, mas ainda não enviou o evento de encerramento/homologação para a API.
  * **Regra de Ouro para o cálculo de Economicidade (Deságio):** O cálculo de deságio (`(valorTotalEstimado - valorTotalHomologado) / valorTotalEstimado`) deve ser feito **apenas** onde `valorTotalHomologado IS NOT NULL AND valorTotalHomologado > 0 AND valorTotalEstimado > 0`.
* **`srp` (Booleano — Sistema de Registro de Preços):**
  * Quando `true`, significa que o valor homologado é um **teto registrado em Ata (ARP)** para compras futuras ao longo de 1 ano, e não um desembolso imediato obrigatório.
* **`situacaoCompraId` e `situacaoCompraNome`:**
  * Indica o status atual do processo: `1 - Divulgada no PNCP`, `2 - Revogada`, `3 - Anulada`, `4 - Suspensa`. Em análises financeiras, deve-se segregar compras *Revogadas/Anuladas* para não inflar os valores.

### 5. Linha do Tempo (Campos de Data)

| Campo de Data | O que representa | Como usar em SQL / dbt |
| :--- | :--- | :--- |
| **`dataPublicacaoPncp`** | Quando a compra foi oficialmente publicada no PNCP. | Eixo principal para análises de **sazonalidade mensal/anual**. |
| **`dataAberturaProposta`** | Início do recebimento de propostas dos fornecedores. | Usado junto com `dataEncerramentoProposta` para medir o prazo dado ao mercado. |
| **`dataEncerramentoProposta`** | Data/hora limite para envio de propostas (abertura da sessão de lances). | Permite saber se o prazo de disputa já passou ou ainda está no futuro. |
| **`dataAtualizacaoGlobal`** | Carimbo de tempo da última alteração daquela compra ou de seus itens/resultados no PNCP. | **Coluna de ordenação na deduplicação (`ROW_NUMBER`)** para garantir a versão mais recente da compra. |

