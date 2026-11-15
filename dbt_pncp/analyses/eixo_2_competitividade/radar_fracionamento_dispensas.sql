SELECT
    ano_compra,
    orgao_razao_social,
    unidade_nome,
    categoria_tic,
    COUNT(DISTINCT numero_controle_pncp) AS qtd_dispensas,
    ROUND(SUM(valor_total_estimado), 2) AS soma_valor_estimado,
    ROUND(SUM(valor_total_homologado), 2) AS soma_valor_homologado
FROM {{ ref('fct_contratacoes') }}
WHERE is_tic = TRUE
  AND modalidade_id = 8
  AND status_processo = 'Homologada'
GROUP BY ano_compra, orgao_razao_social, unidade_nome, categoria_tic
HAVING COUNT(DISTINCT numero_controle_pncp) >= 3
ORDER BY ano_compra DESC, soma_valor_homologado DESC
