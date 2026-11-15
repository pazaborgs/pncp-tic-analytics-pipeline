with stg as (
    select *
    from {{ ref('stg_contratacoes') }}
),

features as (
    select
        *,

        -- Deságios
        case
            when valor_total_homologado > 0 and valor_total_estimado > 0
                then valor_total_estimado - valor_total_homologado
            else null
        end as desagio_absoluto,

        case
            when valor_total_homologado > 0 and valor_total_estimado > 0
                then round(safe_divide(valor_total_estimado - valor_total_homologado, valor_total_estimado) * 100, 2)
            else null
        end as desagio_percentual,

        -- Status do Processo
        case
            when situacao_compra_id in (2, 3, 4)
                then 'Cancelada (Revogada/Anulada/Suspensa)'
            when valor_total_homologado > 0
                then 'Homologada'
            when dt_encerramento_proposta >= current_timestamp()
                then 'Em Andamento'
            else 'Encerrada sem Homologação'
        end as status_processo,

        -- Grupo de Competitividade
        case
            when modalidade_id in (4, 6) then 'Licitação Competitiva'
            when modalidade_id in (8, 9) then 'Contratação Direta'
            else 'Procedimento Auxiliar'
        end as grupo_competitividade,

        -- Esfera e Porte da Contratação
        case orgao_esfera_id
            when 'M' then 'Municipal'
            when 'E' then 'Estadual'
            when 'F' then 'Federal'
            else 'Outros'
        end as orgao_esfera_nome,

        case
            when valor_total_estimado <= 60000 then 'Pequeno Porte (Até R$ 60 mil)'
            when valor_total_estimado <= 500000 then 'Médio Porte (R$ 60 mil a R$ 500 mil)'
            else 'Grande Porte (Acima de R$ 500 mil)'
        end as porte_contratacao,

        -- Sazonalidade e Janela de Propostas
        extract(year from data_publicacao) as ano_publicacao,
        extract(month from data_publicacao) as mes_publicacao,
        extract(quarter from data_publicacao) as trimestre_publicacao,
        (extract(quarter from data_publicacao) = 4) as is_fim_de_ano,
        timestamp_diff(dt_encerramento_proposta, dt_abertura_proposta, day) as dias_janela_proposta

    from stg
)

select *
from features
