SELECT
    ano_publicacao,
    trimestre_publicacao,
    COUNT(DISTINCT numero_controle_pncp) AS total_processos,
    ROUND(SUM(valor_total_estimado), 2) AS soma_valor_estimado,
    ROUND(SUM(valor_total_homologado), 2) AS soma_valor_homologado
FROM {{ ref('fct_contratacoes') }}
WHERE is_tic = TRUE
GROUP BY ano_publicacao, trimestre_publicacao
ORDER BY ano_publicacao ASC, trimestre_publicacao ASC
