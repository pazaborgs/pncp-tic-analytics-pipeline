WITH ranking_extremos AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY orgao_razao_social
            ORDER BY ABS(desagio_percentual) DESC
        ) AS extremo
    FROM {{ ref('fct_contratacoes') }}
    WHERE is_tic = TRUE
      AND status_processo = 'Homologada'
)

SELECT
    numero_controle_pncp,
    orgao_razao_social,
    modalidade_nome,
    categoria_tic,
    objeto_compra,
    ROUND(valor_total_estimado, 2) AS valor_total_estimado,
    ROUND(valor_total_homologado, 2) AS valor_total_homologado,
    ROUND(desagio_percentual, 2) AS desagio_percentual
FROM ranking_extremos
WHERE extremo = 1
ORDER BY ABS(desagio_percentual) DESC
