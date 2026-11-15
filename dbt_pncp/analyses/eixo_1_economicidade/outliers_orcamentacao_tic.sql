WITH outliers_rankeados AS (
    SELECT
        numero_controle_pncp,
        orgao_razao_social,
        modalidade_nome,
        categoria_tic,
        objeto_compra,
        ROUND(valor_total_estimado, 2) AS valor_total_estimado,
        ROUND(valor_total_homologado, 2) AS valor_total_homologado,
        ROUND(desagio_percentual, 2) AS desagio_percentual,
        ROW_NUMBER() OVER (
            ORDER BY valor_total_homologado DESC
        ) AS ranking
    FROM {{ ref('fct_contratacoes') }}
    WHERE is_tic = TRUE
      AND status_processo = 'Homologada'
      AND (desagio_absoluto < 0 OR desagio_percentual > 70)
)

SELECT
    numero_controle_pncp,
    orgao_razao_social,
    modalidade_nome,
    categoria_tic,
    objeto_compra,
    valor_total_estimado,
    valor_total_homologado,
    desagio_percentual
FROM outliers_rankeados
WHERE ranking <= 10
ORDER BY valor_total_homologado DESC
