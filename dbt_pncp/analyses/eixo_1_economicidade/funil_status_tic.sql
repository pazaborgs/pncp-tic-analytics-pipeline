SELECT
    status_processo,
    COUNT(DISTINCT numero_controle_pncp) AS total_processos,
    ROUND(
        (
            COUNT(DISTINCT numero_controle_pncp)
            / NULLIF(SUM(COUNT(DISTINCT numero_controle_pncp)) OVER (), 0)
        ) * 100,
        2
    ) AS percentual_processos,
    ROUND(SUM(valor_total_estimado), 2) AS valor_estimado_acumulado
FROM {{ ref('fct_contratacoes') }}
WHERE is_tic = TRUE
GROUP BY status_processo
ORDER BY total_processos DESC
