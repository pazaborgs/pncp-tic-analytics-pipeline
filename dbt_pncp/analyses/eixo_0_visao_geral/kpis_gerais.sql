SELECT
  ROUND(SUM(valor_total_estimado), 2) AS soma_valor_estimado,
  ROUND(SUM(valor_total_homologado), 2) AS soma_valor_homologado,
  COUNT(DISTINCT numero_controle_pncp) AS total_processos,
  -- ID é unique na teoria, mas uma atualização no contrato pode duplicar a linha no tempo. Pelo dbt, fct_contratacoes ja não é permitida ter duplicatas pelo schema, mas o DISTINCT é uma boa prática preventiva.
  ROUND(AVG(CASE WHEN status_processo = 'Homologada' THEN valor_total_homologado END), 2) AS ticket_medio_homologado
  -- AVG aplica a média e ignora valores NULL por natureza (processo 'Em Andamento' tendem a não ter valor homologado). Tira a média somente dos processos 'Homologado'.
FROM {{ ref('fct_contratacoes')}}
WHERE categoria_tic != 'Não-TIC'
  AND status_processo IN ('Homologada', 'Em Andamento')
