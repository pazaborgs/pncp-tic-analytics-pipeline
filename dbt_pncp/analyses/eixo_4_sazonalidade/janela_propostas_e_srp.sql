SELECT
    modalidade_nome,
    ROUND(AVG(dias_janela_proposta), 1) AS media_dias_janela_proposta,
    COUNT(DISTINCT numero_controle_pncp) AS total_processos,
    SUM(CASE WHEN is_srp = TRUE THEN 1 ELSE 0 END) AS total_processos_srp,
    ROUND(
        SUM(CASE WHEN is_srp = TRUE THEN 1 ELSE 0 END)
        / NULLIF(COUNT(DISTINCT numero_controle_pncp), 0) * 100,
        2
    ) AS percentual_processos_srp
FROM {{ ref('fct_contratacoes') }}
WHERE is_tic = TRUE
GROUP BY modalidade_nome
ORDER BY total_processos DESC
