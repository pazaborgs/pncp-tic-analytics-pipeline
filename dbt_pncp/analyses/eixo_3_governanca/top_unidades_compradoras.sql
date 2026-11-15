WITH gastos_por_unidade AS (
    SELECT
        orgao_razao_social,
        orgao_esfera_nome,
        unidade_nome,
        COUNT(DISTINCT numero_controle_pncp) AS total_processos,
        ROUND(SUM(valor_total_homologado), 2) AS soma_total_homologado
    FROM {{ ref('fct_contratacoes') }}
    WHERE is_tic = TRUE
      AND status_processo = 'Homologada'
    GROUP BY orgao_razao_social, orgao_esfera_nome, unidade_nome
),

ranking_unidades AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            ORDER BY soma_total_homologado DESC
        ) AS ranking
    FROM gastos_por_unidade
)

SELECT
    orgao_razao_social,
    orgao_esfera_nome,
    unidade_nome,
    total_processos,
    soma_total_homologado
FROM ranking_unidades
WHERE ranking <= 10
ORDER BY soma_total_homologado DESC
