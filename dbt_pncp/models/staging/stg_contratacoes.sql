-- Deduplicação dos registros, remoção do camelCase, join com classificação IA e conversão de tipos para a camada Silver (stg_pncp).
WITH source_data AS (
    SELECT
        *
    FROM
        {{ source('bronze_pncp', 'bronze_contratacoes_publicacao') }}
),
deduplicated AS (
    SELECT
        *
    FROM
        source_data
    WHERE
        numeroControlePNCP IS NOT NULL
    QUALIFY row_number() over (
        PARTITION BY numeroControlePNCP
        ORDER BY
            dataAtualizacaoGlobal DESC,
            _ingested_at DESC
    ) = 1
),
classificacao_ia AS (
    SELECT
        numero_controle_pncp,
        cast(is_tic AS bool) AS is_tic,
        categoria_tic,
        safe_cast(_classified_at AS timestamp) AS classified_at
    FROM
        {{ source('bronze_pncp', 'bronze_classificacao_tic_ia') }}
    WHERE
        numero_controle_pncp IS NOT NULL
    QUALIFY row_number() over (
        PARTITION BY numero_controle_pncp
        ORDER BY _classified_at DESC
    ) = 1
),
final AS (
    SELECT
        -- Chaves e Identificadores
        d.numeroControlePNCP AS numero_controle_pncp,
        cast(d.anoCompra AS int64) AS ano_compra,
        cast(d.sequencialCompra AS int64) AS sequencial_compra,
        d.numeroCompra AS numero_compra,
        d.processo AS numero_processo,
        -- Órgão e Unidade Compradora
        d.orgaoEntidade_cnpj AS orgao_cnpj,
        d.orgaoEntidade_razaoSocial AS orgao_razao_social,
        d.orgaoEntidade_poderId AS orgao_poder_id,
        d.orgaoEntidade_esferaId AS orgao_esfera_id,
        d.unidadeOrgao_codigoUnidade AS unidade_codigo,
        d.unidadeOrgao_nomeUnidade AS unidade_nome,
        d.unidadeOrgao_municipioNome AS municipio_nome,
        d.unidadeOrgao_ufSigla AS uf_sigla,
        d.unidadeOrgao_codigoIbge AS codigo_ibge,
        -- Modalidade, Disputa e Amparo Legal
        cast(d.modalidadeId AS int64) AS modalidade_id,
        d.modalidadeNome AS modalidade_nome,
        cast(d.modoDisputaId AS int64) AS modo_disputa_id,
        d.modoDisputaNome AS modo_disputa_nome,
        d.tipoInstrumentoConvocatorioNome AS instrumento_convocatorio_nome,
        d.amparoLegal_codigo AS amparo_legal_codigo,
        d.amparoLegal_nome AS amparo_legal_nome,
        d.amparoLegal_descricao AS amparo_legal_descricao,
        -- Situação, Objeto e Características da Compra
        cast(d.situacaoCompraId AS int64) AS situacao_compra_id,
        d.situacaoCompraNome AS situacao_compra_nome,
        cast(d.srp AS bool) AS is_srp,
        d.objetoCompra AS objeto_compra,
        d.informacaoComplementar AS informacao_complementar,
        -- Classificação Semântica de TIC (IA)
        ia.is_tic,
        ia.categoria_tic,
        ia.classified_at,
        -- Valores Financeiros
        cast(d.valorTotalEstimado AS numeric) AS valor_total_estimado,
        cast(d.valorTotalHomologado AS numeric) AS valor_total_homologado,
        -- Datas e Timestamps
        safe_cast(d.dataPublicacaoPncp AS timestamp) AS dt_publicacao_pncp,
        date(safe_cast(d.dataPublicacaoPncp AS timestamp)) AS data_publicacao,
        safe_cast(d.dataAberturaProposta AS timestamp) AS dt_abertura_proposta,
        safe_cast(d.dataEncerramentoProposta AS timestamp) AS dt_encerramento_proposta,
        safe_cast(d.dataAtualizacaoGlobal AS timestamp) AS dt_atualizacao_global,
        -- Metadados de Engenharia
        d._row_hash,
        date(d._load_date) AS load_date,
        d._source_file AS source_file,
        safe_cast(d._ingested_at AS timestamp) AS ingested_at
    FROM
        deduplicated AS d
    LEFT JOIN
        classificacao_ia AS ia
        ON d.numeroControlePNCP = ia.numero_controle_pncp
)
SELECT
    *
FROM
    final
