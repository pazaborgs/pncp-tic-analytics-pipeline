# Resultados Consolidados das Análises SQL (`marts_pncp.fct_contratacoes`)

Total de consultas executadas: **14**

## `eixo_0_visao_geral/kpis_gerais.sql` (1 linhas)

| soma_valor_estimado | soma_valor_homologado | total_processos | ticket_medio_homologado |
| --- | --- | --- | --- |
| 260.287.356,74 | 143.305.869,15 | 247 | 604.666,11 |

---

## `eixo_0_visao_geral/percentual_categoria_tic.sql` (4 linhas)

| categoria_tic | total_processos | soma_total_homologado | percentual_processos | percentual_soma_homologado |
| --- | --- | --- | --- | --- |
| Serviços de TI | 35 | 61.969.435,68 | 14,17 | 43,24 |
| Redes, Cloud e Segurança | 50 | 32.648.135,64 | 20,24 | 22,78 |
| Software e Licenciamento | 28 | 32.588.785,02 | 11,34 | 22,74 |
| Hardware e Equipamentos | 134 | 16.099.512,81 | 54,25 | 11,23 |

---

## `eixo_1_economicidade/desagio_tic_e_nao_tic.sql` (5 linhas)

| categoria_tic | total_processos_homologados | desagio_absoluto_medio | desagio_percentual_medio | desagio_percentual_max | desagio_percentual_min |
| --- | --- | --- | --- | --- | --- |
| Redes, Cloud e Segurança | 31 | 587.047,85 | 41,98 | 93,34 | 0,00 |
| Software e Licenciamento | 12 | 2.081.030,58 | 37,70 | 69,92 | 0,00 |
| Não-TIC | 2604 | 394.247,73 | 33,86 | 99,98 | -542,01 |
| Hardware e Equipamentos | 82 | 52.131,11 | 32,17 | 84,14 | 0,00 |
| Serviços de TI | 28 | 1.208.902,28 | 30,85 | 67,51 | 0,00 |

---

## `eixo_1_economicidade/economia_anual_tic.sql` (3 linhas)

| ano_publicacao | total_processos | soma_valor_estimado | soma_valor_homologado | economia_gerada_total | desagio_medio_simples | desagio_medio_ponderado |
| --- | --- | --- | --- | --- | --- | --- |
| 2024 | 54 | 11.742.797,83 | 9.722.598,41 | 2.046.583,46 | 24,06 | 17,43 |
| 2025 | 109 | 88.958.208,05 | 59.409.820,38 | 29.552.206,07 | 34,40 | 33,22 |
| 2026 | 74 | 124.067.993,33 | 74.173.450,36 | 49.894.542,97 | 27,40 | 40,22 |

---

## `eixo_1_economicidade/funil_status_tic.sql` (4 linhas)

| status_processo | total_processos | percentual_processos | valor_estimado_acumulado |
| --- | --- | --- | --- |
| Homologada | 237 | 67,14 | 224.768.999,21 |
| Encerrada sem Homologação | 99 | 28,05 | 89.324.616,68 |
| Em Andamento | 10 | 2,83 | 35.518.357,53 |
| Cancelada (Revogada/Anulada/Suspensa) | 7 | 1,98 | 466.792,01 |

---

## `eixo_1_economicidade/maior_extremo_por_orgao.sql` (15 linhas)

| numero_controle_pncp | orgao_razao_social | modalidade_nome | categoria_tic | objeto_compra | valor_total_estimado | valor_total_homologado | desagio_percentual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 49203409000102-1-000038/2026 | CAMARA MUNICIPAL DE SANTOS | Pregão - Eletrônico | Redes, Cloud e Segurança | Contratação de empresa para prestação de serviço de Telefonia Fixa Comutada  STFC fixofixo e fixomóvel, com fornecimento de Tronco SIP nos termos das concessões outorgadas pela Agência Nacional de Telecomunicações-ANATEL, para atender às necessidades de comunicação da Câmara Municipal de Santos, conforme especificações técnicas constantes do Termo de Referência Anexo I do Edital. | 120.148,80 | 7.999,92 | 93,34 |
| 46374500000194-1-007290/2025 | SECRETARIA DE ESTADO DA SAUDE | Pregão - Eletrônico | Redes, Cloud e Segurança | Contratação de pacote de internet com comodato de aparelhos  | 40.080,00 | 2.952,00 | 92,63 |
| 00394502000144-1-019491/2024 | COMANDO DA MARINHA | Inexigibilidade | Redes, Cloud e Segurança | Serviços de provedor de rede MPLS/SD-WAN para transmissão de dados, voz e vídeo incluindo hardware, software, enlace de transmissão de dados, serviços de gerência e demais serviços associados, velocidade garantida, banda de 34Mbps, atendimento 24x7, fornecimento de roteador Cisco. | 106.539,36 | 8.750,00 | 91,79 |
| 58200015000183-1-000305/2025 | MUNICIPIO DE SANTOS | Pregão - Eletrônico | Hardware e Equipamentos | Aquisição de fones de ouvido sem fio bluetooth para a UME Florestan Fernandes I, da Secretaria Municipal de Educação - SEDUC, conforme descrição constante no Anexo I – Termo de Referência do Edital. | 50.023,20 | 7.934,40 | 84,14 |
| 46377800000127-1-004132/2024 | SAO PAULO SECRETARIA DA SEGURANCA PUBLICA | Pregão - Eletrônico | Hardware e Equipamentos | Aquisição de suprimentos de informática para o 2º BAEP | 13.621,06 | 3.168,60 | 76,74 |
| 15563047000130-1-000006/2025 | FUNDACAO PARQUE TECNOLOGICO DE SANTOS | Dispensa | Redes, Cloud e Segurança | [LICITANET] - Contratação de solução de telefonia VoIP baseada em PABX virtual, em nuvem, incluindo implantação, configuração e suporte, mediante licenciamento para 10 usuários, pelo período de 12 (doze) meses.  | 4.800,00 | 1.600,00 | 66,67 |
| 44837524000107-1-000033/2026 | COMPANHIA DOCAS DO ESTADO DE SAO PAULO | Pregão - Eletrônico | Redes, Cloud e Segurança | Contratação de pessoa jurídica para a prestação dos serviços de Sistema de Radiocomunicação para Autoridade Portuária de Santos com vigência contratual, pelo prazo de 36 (trinta e seis) meses, nos termos e condições estabelecidas no "Termo de Referência" e seus Anexos, partes integrantes deste Edital. | 9.507.420,00 | 3.219.876,00 | 66,13 |
| 00034616000183-1-000004/2026 | COMPANHIA DE ENGENHARIA DE TRAFEGO DE SANTOS - CET - SANTOS | Pregão - Eletrônico | Hardware e Equipamentos | Seleção de propostas para REGISTRO DE PREÇOS visando a aquisição de computadores completos, acompanhados de sistema operacional, Microsoft Office e softwares do fabricante, conforme Termo de Referência, Anexos I e I.A do Edital. | 718.800,00 | 365.986,69 | 49,08 |
| 58197948000169-1-000027/2024 | CAIXA DE ASSISTENCIA  AO SERVIDOR PUBLICO MUNICIPAL DE SANTOS - CAPEP-SAUDE | Pregão - Eletrônico | Hardware e Equipamentos | Seleção de PROPOSTAS PARA REGISTRO DE PREÇOS visando à prestação de serviços de LOCAÇÃO MENSAL DE EQUIPAMENTOS DE INFORMATICA (microcomputador, monitor, teclado, mouse, estabilizador, pacote office e sistema operacional), incluindo suporte técnico e manutenção preventiva e corretiva, conforme condições, exigências e descrição constante no Anexo I - Termo de Referência do Edital. | 456,64 | 247,80 | 45,73 |
| 46384111000140-1-001565/2025 | SAO PAULO SECRETARIA DA EDUCACAO | Dispensa | Hardware e Equipamentos | 1.1.	Aquisição de adaptador hdmi/dispolayport, bloco adesivo, capa de processo, maleta arquivo, caixa arquivo morto, envelope plástico, envelope papel kraft, grampo plástico, pasta polionda com elástico, café torrado e moído, pen drive de 32gb, chá mate a granel, bateria alcalina de 9v, garrafa térmica de 1,8l, pasta L,  e pasta suspensa,   | 12.431,73 | 6.807,80 | 45,24 |
| 58158635000100-1-000001/2026 | Companhia de Habitação da Baixada Santista/SP | Pregão - Eletrônico | Redes, Cloud e Segurança | A contratação de empresa especializada para prestação de Serviço Telefônico Fixo Comutado (STFC) por meio de solução completa de PABX em nuvem (Cloud PABX), incluindo implantação, configuração, migração, disponibilização de ramais virtuais, suporte técnico, operação assistida, manutenção preventiva e corretiva, bem como fornecimento de funcionalidades avançadas de gestão e monitoramento, visando à modernização e integração e unificação do sistema de telefonia corporativa da Companhia de Habitaçã | 84.480,00 | 54.133,84 | 35,92 |
| 01446932000125-1-000014/2026 | FUNDACAO ARQUIVO E MEMORIA DE SANTOS | Dispensa | Software e Licenciamento | Aquisição de licença de uso do software AutoCad LT, em modalidade de assinatura anual, pelo período de 12 (doze) meses, destinada ao atendimento das necessidades do Acervo Cartográfico da FAMS. | 2.455,55 | 1.946,00 | 20,75 |
| 08717299000101-1-000026/2024 | INSTITUTO DE PREVIDENCIA SOCIAL DOS SERVIDORES PUBLICOS MUNICIPAIS DE SANTOS | Pregão - Eletrônico | Hardware e Equipamentos | O objeto da presente licitação é a aquisição de 15 computadores, 28 monitores (21  polegadas), 15 mouses e 15 teclados, e 15 licenças de software (office/windows) conforme especificações padronizadas pelo Departamento de Tecnologia da Informação da Prefeitura Municipal de Santos. (DETIC-PMS), especificadas no termo de referência - Anexo I do edital | 95.764,74 | 77.845,19 | 18,71 |
| 46377222000129-1-000116/2024 | SECRETARIA DA FAZENDA E PLANEJAMENTO | Pregão - Eletrônico | Redes, Cloud e Segurança | Prestação de serviço de monitoramento com circuito fechado de CFTV, controle de acesso, sistema de alarmes e detecção de incêndio em regime de tempo integral (24x7) na Regional de Santos e a unidade de Praia Grande, conforme condições quantidades e exigências estabelecidas no Edital e seus Anexos. | 709.357,20 | 659.989,80 | 6,96 |
| 47209002000159-1-000014/2026 | SECRETARIA DA HABITACAO | Dispensa | Serviços de TI | Constituiu objeto do presente contrato a prestação de serviços de gestão em soluções e produtos de tecnologia da informação e comunicação nas áreas de desenvolvimento, produção, armazenamento, infraestrutura, manutenção, processamento e guarda de sistemas, dados, informações e documentos, por meio da utilização de ferramentas, processos e ativos de tecnologia da informação e comunicação. | 14.119,20 | 14.119,20 | 0,00 |

---

## `eixo_1_economicidade/outliers_orcamentacao_tic.sql` (10 linhas)

| numero_controle_pncp | orgao_razao_social | modalidade_nome | categoria_tic | objeto_compra | valor_total_estimado | valor_total_homologado | desagio_percentual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 58200015000183-1-000526/2025 | MUNICIPIO DE SANTOS | Pregão - Eletrônico | Redes, Cloud e Segurança | Contratação de empresa especializada para prestação de serviços mensais de conectividade IP (Internet Protocol), consistindo no fornecimento de acesso IP dedicado à Internet em 03 (três) conexões com links redundantes (principal e redundantes) a serem instalados no datacenter da Prefeitura Municipal de Santos (Paço Municipal), pelo período de 05 (cinco) anos, podendo ser prorrogado por sucessivo período, até limite da Lei Federal 14.133/21 - Arts. 106 e 107. | 3.762.219,60 | 889.560,00 | 76,36 |
| 49203409000102-1-000018/2025 | CAMARA MUNICIPAL DE SANTOS | Pregão - Eletrônico | Redes, Cloud e Segurança | Contratação de serviços de videoconferência em nuvem para realização, gravação e transmissão ao vivo, das sessões Ordinárias, Extraordinárias, Audiências Públicas, Câmaras Jovens, Escola do Legislativo bem como as Sessões Solenes da Câmara Municipal de Santos, sendo estas armazenadas e posteriormente disponibilizadas no site do Órgão, conforme especificações técnicas constantes do Termo de Referência (Anexo I do Edital). | 194.267,52 | 53.916,60 | 72,25 |
| 58200015000183-1-000338/2026 | MUNICIPIO DE SANTOS | Pregão - Eletrônico | Hardware e Equipamentos | Aquisição de microcomputadores completos tipo (desktop e workstation), smartphones e tablets, para atendimento das demandas da Coordenadoria de Fiscalização de Posturas, da Secretaria Municipal das Prefeituras Regionais - SEPREF. | 193.627,93 | 41.381,97 | 78,63 |
| 49203409000102-1-000022/2024 | CAMARA MUNICIPAL DE SANTOS | Pregão - Eletrônico | Redes, Cloud e Segurança | Contratação de empresa especializada para a prestação de serviços de telecomunicações de 02 (dois) “links” dedicados de acesso à internet, em conformidade com as especificações constantes nos termos de concessões outorgadas pela Agência Nacional de Telecomunicações – ANATEL, conforme especificações técnicas constantes do Termo de Referência (Anexo I do Edital). | 150.522,00 | 15.210,00 | 89,90 |
| 00394502000144-1-019491/2024 | COMANDO DA MARINHA | Inexigibilidade | Redes, Cloud e Segurança | Serviços de provedor de rede MPLS/SD-WAN para transmissão de dados, voz e vídeo incluindo hardware, software, enlace de transmissão de dados, serviços de gerência e demais serviços associados, velocidade garantida, banda de 34Mbps, atendimento 24x7, fornecimento de roteador Cisco. | 106.539,36 | 8.750,00 | 91,79 |
| 49203409000102-1-000038/2026 | CAMARA MUNICIPAL DE SANTOS | Pregão - Eletrônico | Redes, Cloud e Segurança | Contratação de empresa para prestação de serviço de Telefonia Fixa Comutada  STFC fixofixo e fixomóvel, com fornecimento de Tronco SIP nos termos das concessões outorgadas pela Agência Nacional de Telecomunicações-ANATEL, para atender às necessidades de comunicação da Câmara Municipal de Santos, conforme especificações técnicas constantes do Termo de Referência Anexo I do Edital. | 120.148,80 | 7.999,92 | 93,34 |
| 58200015000183-1-000305/2025 | MUNICIPIO DE SANTOS | Pregão - Eletrônico | Hardware e Equipamentos | Aquisição de fones de ouvido sem fio bluetooth para a UME Florestan Fernandes I, da Secretaria Municipal de Educação - SEDUC, conforme descrição constante no Anexo I – Termo de Referência do Edital. | 50.023,20 | 7.934,40 | 84,14 |
| 46374500000194-1-007677/2026 | SECRETARIA DE ESTADO DA SAUDE | Pregão - Eletrônico | Redes, Cloud e Segurança | CONTRATAÇÃO DE EMPRESA ESPECIALIZADA EM TELEFONIA MÓVEL COM COMODATO DE EQUIPAMENTOS | 44.400,00 | 7.200,00 | 83,78 |
| 58200015000183-1-000187/2025 | MUNICIPIO DE SANTOS | Pregão - Eletrônico | Hardware e Equipamentos | Aquisição de fones de ouvido do tipo headset para as Unidades Municipais que atendem os alunos da Educação de Jovens e Adultos (EJA), da Secretaria Municipal de Educação - SEDUC, conforme descrição constante no Anexo I – Termo de Referência do Edital. | 16.150,50 | 4.200,00 | 73,99 |
| 49203409000102-1-000001/2025 | CAMARA MUNICIPAL DE SANTOS | Pregão - Eletrônico | Redes, Cloud e Segurança | Seleção de propostas para registro de preços visando a contratação de serviços de emissão de certificados digitais do tipo A3, padrão ICP-Brasil, e-CPF e e-CNPJ, com fornecimento e mídia de armazenamento (token), conforme descrições constantes no Termo de Referência, Anexo I do Edital.  | 12.309,84 | 3.480,00 | 71,73 |

---

## `eixo_2_competitividade/amparos_legais_direta.sql` (6 linhas)

| modalidade_nome | amparo_legal_nome | amparo_legal_descricao | total_processos | soma_total_homologado |
| --- | --- | --- | --- | --- |
| Dispensa | Lei 14.133/2021, Art. 75, VIII | Dispensa de Licitação: nos casos de emergência ou de calamidade pública, quando caracterizada urgência de atendimento de situação que possa ocasionar prejuízo ou comprometer a continuidade dos serviços públicos ou a segurança de pessoas, obras, serviços, equipamentos e outros bens, públicos ou particulares, e somente para aquisição dos bens necessários ao atendimento da situação emergencial ou calamitosa e para as parcelas de obras e serviços que possam ser concluídas no prazo máximo de 1 (um) ano, contado da data de ocorrência da emergência ou da calamidade, vedadas a prorrogação dos respectivos contratos e a recontratação de empresa já contratada com base no disposto neste inciso | 1 | 532.800,00 |
| Dispensa | Lei 14.133/2021, Art. 75, II | Dispensa de Licitação: para contratação que envolva valores inferiores a R$ 50.000,00 (cinquenta mil reais), no caso de outros serviços e compras | 72 | 424.041,98 |
| Dispensa | Lei 14.133/2021, Art. 75, IX | Dispensa de Licitação: para a aquisição, por pessoa jurídica de direito público interno, de bens produzidos ou serviços prestados por órgão ou entidade que integrem a Administração Pública e que tenham sido criados para esse fim específico, desde que o preço contratado seja compatível com o praticado no mercado | 4 | 423.419,76 |
| Dispensa | Lei 14.133/2021, Art. 75, XV | Dispensa de Licitação: para contratação de instituição brasileira que tenha por finalidade estatutária apoiar, captar e executar atividades de ensino, pesquisa, extensão, desenvolvimento institucional, científico e tecnológico e estímulo à inovação, inclusive para gerir administrativa e financeiramente essas atividades, ou para contratação de instituição dedicada à recuperação social da pessoa presa, desde que o contratado tenha inquestionável reputação ética e profissional e não tenha fins lucrativos | 1 | 191.456,00 |
| Inexigibilidade | Lei 14.133/2021, Art. 74, I | Inexigibilidade de Licitação: aquisição de materiais, de equipamentos ou de gêneros ou contratação de serviços que só possam ser fornecidos por produtor, empresa ou representante comercial exclusivos | 5 | 142.728,08 |
| Dispensa | Lei 13.303/2016, Art. 29, II | Dispensa de Licitação: para outros serviços e compras de valor até R$ 50.000,00 (cinquenta mil reais) e para alienações, nos casos previstos nesta Lei, desde que não se refiram a parcelas de um mesmo serviço, compra ou alienação de maior vulto que possa ser realizado de uma só vez | 1 | 18.400,00 |

---

## `eixo_2_competitividade/competitividade_por_categoria.sql` (12 linhas)

| categoria_tic | modalidade_nome | total_processos | soma_total_homologado | percentual_dinheiro_categoria |
| --- | --- | --- | --- | --- |
| Hardware e Equipamentos | Pregão - Eletrônico | 82 | 15.801.386,80 | 98,15 |
| Hardware e Equipamentos | Dispensa | 46 | 271.126,01 | 1,68 |
| Hardware e Equipamentos | Inexigibilidade | 1 | 27.000,00 | 0,17 |
| Redes, Cloud e Segurança | Pregão - Eletrônico | 31 | 32.595.539,49 | 99,84 |
| Redes, Cloud e Segurança | Dispensa | 16 | 43.846,15 | 0,13 |
| Redes, Cloud e Segurança | Inexigibilidade | 1 | 8.750,00 | 0,03 |
| Serviços de TI | Pregão - Eletrônico | 28 | 61.352.552,94 | 99,00 |
| Serviços de TI | Dispensa | 6 | 616.882,74 | 1,00 |
| Software e Licenciamento | Pregão - Eletrônico | 11 | 25.825.544,53 | 79,25 |
| Software e Licenciamento | Concorrência - Eletrônica | 1 | 5.997.999,57 | 18,41 |
| Software e Licenciamento | Dispensa | 11 | 658.262,84 | 2,02 |
| Software e Licenciamento | Inexigibilidade | 3 | 106.978,08 | 0,33 |

---

## `eixo_2_competitividade/radar_fracionamento_dispensas.sql` (4 linhas)

| ano_compra | orgao_razao_social | unidade_nome | categoria_tic | qtd_dispensas | soma_valor_estimado | soma_valor_homologado |
| --- | --- | --- | --- | --- | --- | --- |
| 2026 | MUNICIPIO DE SANTOS | MSP-PREFEITURA MUNICIPAL DE SANTOS | Hardware e Equipamentos | 5 | 59.969,19 | 56.174,81 |
| 2025 | MUNICIPIO DE SANTOS | MSP-PREFEITURA MUNICIPAL DE SANTOS | Hardware e Equipamentos | 10 | 43.848,42 | 27.257,47 |
| 2025 | MUNICIPIO DE SANTOS | MSP-PREFEITURA MUNICIPAL DE SANTOS | Redes, Cloud e Segurança | 4 | 15.336,68 | 6.842,07 |
| 2024 | MUNICIPIO DE SANTOS | SECRETARIA DE GESTAO | Hardware e Equipamentos | 7 | 27.312,79 | 18.127,24 |

---

## `eixo_3_governanca/escala_porte_vs_desagio.sql` (3 linhas)

| porte_contratacao | total_processos | desagio_percentual_medio | soma_desagio_absoluto |
| --- | --- | --- | --- |
| Médio Porte (R$ 60 mil a R$ 500 mil) | 43 | 36,38 | 2.931.006,76 |
| Pequeno Porte (Até R$ 60 mil) | 75 | 35,21 | 580.207,68 |
| Grande Porte (Acima de R$ 500 mil) | 35 | 29,99 | 77.783.650,63 |

---

## `eixo_3_governanca/top_unidades_compradoras.sql` (10 linhas)

| orgao_razao_social | orgao_esfera_nome | unidade_nome | total_processos | soma_total_homologado |
| --- | --- | --- | --- | --- |
| COMPANHIA DOCAS DO ESTADO DE SAO PAULO | Federal | GELIC-GERÊNCIA DE LICITAÇÃO E CONTRATOS | 11 | 62.868.749,01 |
| MUNICIPIO DE SANTOS | Municipal | MSP-PREFEITURA MUNICIPAL DE SANTOS | 50 | 31.482.554,42 |
| MUNICIPIO DE SANTOS | Municipal | Prefeitura Municipal de Santos | 6 | 20.938.188,65 |
| MUNICIPIO DE SANTOS | Municipal | SECRETARIA DE GESTAO | 18 | 7.494.385,52 |
| SECRETARIA DE ESTADO DA SAUDE | Estadual | ESP-HOSP. GUILHERME ALVARO, SANTOS | 33 | 4.054.537,23 |
| CAMARA MUNICIPAL DE SANTOS | Municipal | CAMARA MUNICIPAL DE SANTOS | 11 | 4.016.793,92 |
| MUNICIPIO DE SANTOS | Municipal | GERAL | 11 | 3.184.800,41 |
| CAMARA MUNICIPAL DE SANTOS | Municipal | CÂMARA MUNICIPAL DE SANTOS - SP | 12 | 1.721.465,58 |
| MUNICIPIO DE SANTOS | Municipal | SECRETARIA MUNICIPAL DE SAUDE | 5 | 1.554.646,91 |
| SAO PAULO SECRETARIA DA SEGURANCA PUBLICA | Estadual | ESP-COMANDO POLIC.INT.-6 SANTOS | 22 | 910.395,58 |

---

## `eixo_4_sazonalidade/janela_propostas_e_srp.sql` (4 linhas)

| modalidade_nome | media_dias_janela_proposta | total_processos | total_processos_srp | percentual_processos_srp |
| --- | --- | --- | --- | --- |
| Pregão - Eletrônico | 17,00 | 228 | 18 | 7,89 |
| Dispensa | 6,60 | 116 | 1 | 0,86 |
| Inexigibilidade |  | 6 | 0 | 0,00 |
| Concorrência - Eletrônica | 41,30 | 3 | 0 | 0,00 |

---

## `eixo_4_sazonalidade/sazonalidade_trimestral_tic.sql` (12 linhas)

| ano_publicacao | trimestre_publicacao | total_processos | soma_valor_estimado | soma_valor_homologado |
| --- | --- | --- | --- | --- |
| 2024 | 1 | 2 | 32.706,73 | 28.231,00 |
| 2024 | 2 | 17 | 3.246.128,84 | 2.498.850,15 |
| 2024 | 3 | 32 | 2.601.417,76 | 1.553.601,91 |
| 2024 | 4 | 30 | 6.524.710,09 | 5.641.915,35 |
| 2025 | 1 | 22 | 21.211.343,07 | 6.713.142,24 |
| 2025 | 2 | 37 | 31.993.777,06 | 26.312.128,07 |
| 2025 | 3 | 50 | 32.390.823,42 | 13.168.647,14 |
| 2025 | 4 | 35 | 17.011.460,37 | 13.215.902,93 |
| 2026 | 1 | 21 | 95.063.619,26 | 57.260.773,70 |
| 2026 | 2 | 32 | 27.144.680,83 | 13.092.380,32 |
| 2026 | 3 | 40 | 56.571.426,82 | 2.427.625,46 |
| 2026 | 4 | 35 | 56.286.671,18 | 1.392.670,88 |

---
