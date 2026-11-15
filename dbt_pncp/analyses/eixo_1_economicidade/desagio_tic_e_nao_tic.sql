SELECT
  categoria_tic,
  COUNT(DISTINCT numero_controle_pncp) AS total_processos_homologados,
  ROUND(AVG(desagio_absoluto), 2) AS desagio_absoluto_medio,
  ROUND(AVG(desagio_percentual), 2) AS desagio_percentual_medio,
  MAX(desagio_percentual) AS desagio_percentual_max,
  MIN(desagio_percentual) AS desagio_percentual_min
FROM {{ ref('fct_contratacoes')}}
WHERE grupo_competitividade = 'Licitação Competitiva'
  AND status_processo = 'Homologada'
GROUP BY categoria_tic
ORDER BY desagio_percentual_medio DESC
