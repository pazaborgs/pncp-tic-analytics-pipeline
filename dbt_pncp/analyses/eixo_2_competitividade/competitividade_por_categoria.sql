SELECT
    categoria_tic,
    modalidade_nome,
    COUNT(DISTINCT numero_controle_pncp) AS total_processos,
    ROUND(SUM(valor_total_homologado), 2) AS soma_total_homologado,
    ROUND(
        SUM(valor_total_homologado)
        / NULLIF(SUM(SUM(valor_total_homologado)) OVER (PARTITION BY categoria_tic), 0) * 100,
        2
    ) AS percentual_dinheiro_categoria
FROM {{ ref('fct_contratacoes') }}
WHERE is_tic = TRUE
  AND grupo_competitividade IN ('Licitação Competitiva', 'Contratação Direta')
  AND status_processo = 'Homologada'
GROUP BY categoria_tic, modalidade_nome
ORDER BY categoria_tic, soma_total_homologado DESC
