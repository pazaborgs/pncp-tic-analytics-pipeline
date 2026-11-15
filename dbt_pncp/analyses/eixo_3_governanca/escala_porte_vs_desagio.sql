SELECT
    porte_contratacao,
    COUNT(DISTINCT numero_controle_pncp) AS total_processos,
    ROUND(AVG(desagio_percentual), 2) AS desagio_percentual_medio,
    ROUND(SUM(desagio_absoluto), 2) AS soma_desagio_absoluto
FROM {{ ref('fct_contratacoes') }}
WHERE is_tic = TRUE
  AND status_processo = 'Homologada'
  AND grupo_competitividade = 'Licitação Competitiva'
GROUP BY porte_contratacao
ORDER BY desagio_percentual_medio DESC
