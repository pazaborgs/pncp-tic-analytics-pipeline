SELECT
  categoria_tic,
  COUNT(DISTINCT numero_controle_pncp) AS total_processos,
  ROUND(SUM(valor_total_homologado), 2) AS soma_total_homologado,

  ROUND(
    (COUNT(DISTINCT numero_controle_pncp) /
    NULLIF(SUM(COUNT(DISTINCT numero_controle_pncp)) OVER (), 0)) * 100
  , 2) AS percentual_processos,

  ROUND(SUM(valor_total_homologado) / NULLIF(SUM(SUM(valor_total_homologado)) OVER(), 0) * 100, 2) AS percentual_soma_homologado

FROM {{ ref('fct_contratacoes')}}
WHERE categoria_tic != 'Não-TIC'
  AND status_processo IN ('Homologada', 'Em Andamento')
GROUP BY
  categoria_tic
ORDER BY
  soma_total_homologado DESC
