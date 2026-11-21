WITH gastos_por_orgao AS (
    SELECT
        orgao_razao_social,
        orgao_esfera_nome,
        COUNT(DISTINCT unidade_nome) AS qtd_unidades,
        COUNT(DISTINCT numero_controle_pncp) AS total_processos,
        ROUND(SUM(valor_total_homologado), 2) AS soma_total_homologado
    FROM {{ ref('fct_contratacoes') }}
    WHERE is_tic = TRUE
      AND status_processo = 'Homologada'
    GROUP BY orgao_razao_social, orgao_esfera_nome
),

ranking_orgaos AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            ORDER BY soma_total_homologado DESC
        ) AS ranking
    FROM gastos_por_orgao
)

SELECT
    orgao_razao_social,
    orgao_esfera_nome,
    qtd_unidades,
    total_processos,
    soma_total_homologado
FROM ranking_orgaos
WHERE ranking <= 10
ORDER BY soma_total_homologado DESC
