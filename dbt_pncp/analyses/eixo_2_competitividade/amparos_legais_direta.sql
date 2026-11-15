SELECT
    modalidade_nome,
    amparo_legal_nome,
    amparo_legal_descricao,
    COUNT(DISTINCT numero_controle_pncp) AS total_processos,
    ROUND(SUM(valor_total_homologado), 2) AS soma_total_homologado
FROM {{ ref('fct_contratacoes') }}
WHERE is_tic = TRUE
  AND grupo_competitividade = 'Contratação Direta'
  AND status_processo = 'Homologada'
GROUP BY
    modalidade_nome,
    amparo_legal_nome,
    amparo_legal_descricao
ORDER BY
    soma_total_homologado DESC
