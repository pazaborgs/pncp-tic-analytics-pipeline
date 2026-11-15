SELECT
  ano_publicacao,
  COUNT(DISTINCT numero_controle_pncp) AS total_processos,
  ROUND(SUM(valor_total_estimado), 2) AS soma_valor_estimado,
  ROUND(SUM(valor_total_homologado), 2) AS soma_valor_homologado,
  ROUND(SUM(desagio_absoluto), 2) AS economia_gerada_total,
  ROUND(AVG(desagio_percentual), 2) AS desagio_medio_simples,
  ROUND(
    (SUM(desagio_absoluto) / NULLIF(SUM(valor_total_estimado), 0)) * 100
  , 2) AS desagio_medio_ponderado
FROM {{ ref('fct_contratacoes')}}
WHERE categoria_tic != 'Não-TIC'
  AND status_processo IN ('Homologada')
GROUP BY ano_publicacao
ORDER BY ano_publicacao ASC
