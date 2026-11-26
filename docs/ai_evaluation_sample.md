# Amostra Estratificada para Avaliação da IA (50 Contratações - 10 por Categoria)

Semente aleatória fixa (`random_state=42`) para reprodutibilidade estatística (`src/classification/evaluate_sample.py`).

## Resumo Estatístico da Auditoria Humana ($n = 50$)

| Estrato ($h$) | Total na Base ($N_h$) | Peso no Universo TIC ($W_{\text{tic}}$) | Amostra ($n_h$) | Precisão Binária (`is_tic`) | Precisão de Subcategoria | Divergências Identificadas |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Software e Licenciamento** | 44 | 12,5% | 10 | **80%** (8/10) | **80%** (8/10) | Itens **#9** (benefício RH/academia) e **#10** (chamada de enfermagem hospitalar) são `Não-TIC`. |
| **Redes, Cloud e Segurança** | 67 | 19,0% | 10 | **100%** (10/10) | **90%** (9/10) | Item **#17** (nobreak) é TIC, porém pertence a `Hardware e Equipamentos`. |
| **Serviços de TI** | 52 | 14,7% | 10 | **80%** (8/10) | **80%** (8/10) | Itens **#22** (produção audiovisual/TV Câmara) e **#23** (palestras de empreendedorismo) são `Não-TIC`. |
| **Hardware e Equipamentos** | 190 | 53,8% | 10 | **90%** (9/10) | **90%** (9/10) | Item **#37** (drone para pulverização de larvicida) é `Não-TIC` (vigilância epidemiológica). |
| **Não-TIC** | 4.835 | — | 10 | **100%** (10/10) | **100%** (10/10) | Nenhuma divergência (0 falsos negativos na amostra). |

### Métricas Consolidadas (Estimador Estratificado Ponderado $\hat{P}_{st} = \sum W_h \hat{p}_h$)
- **Precisão Positiva Ponderada (`is_tic = True`):** $\mathbf{89,2\%}$ ($\pm 5,97\%$ de erro padrão estratificado) $\rightarrow$ estima-se $\approx 315$ processos estritamente de TIC dentre os 353 sinalizados.
- **Fidelidade de Subcategoria (dentre os Verdadeiros Positivos):** $\mathbf{97,1\%}$ ($34 / 35$).
- **Acurácia Global Ponderada ($N = 5.188$):** $\mathbf{99,26\%}$.

---

## Amostras

1. **[Software e Licenciamento]** (58200015000183-1-000497/2026)
   - **Objeto:** Aquisição de Licença anual do Software Canva Pro, visando atender às necessidades da Seção de Compostagem – COPOLAM/DEPCAM/SEMAM da Secretaria Municipal de Meio Ambiente, Desenvolvimento Urbano e Sustentabilidade - SEMAM.


2. **[Software e Licenciamento]** (58200015000183-1-000624/2026)
   - **Objeto:** Aquisição de vestuário institucional (camisetas e coletes de identificação), equipamentos multimídia e de informática (projetor, microcomputador portátil tipo notebook e licença de software - microsoft office home & business 2021), para serem utilizados [...]

3. **[Software e Licenciamento]** (58200015000183-1-000052/2024)
   - **Objeto:** Contratação de serviços contínuos de plataforma para assinatura digital, mediante disponibilização de licenças de uso de solução de tecnologia, com treinamento de pessoal, para o Departamento de Registro de Atos Oficiais do Gabinete do Prefeito Municipal, pelo período de 12 (doze) meses, podendo ser prorrogado por iguais e sucessivos períodos até o limite de 60 (sessenta) meses.

4. **[Software e Licenciamento]** (01446932000125-1-000014/2026)
   - **Objeto:** Aquisição de licença de uso do software AutoCad LT, em modalidade de assinatura anual, pelo período de 12 (doze) meses, destinada ao atendimento das necessidades do Acervo Cartográfico da FAMS.

5. **[Software e Licenciamento]** (01446932000125-1-000011/2026)
   - **Objeto:** Aquisição de 03 (três) licenças ADOBE CRIATIVE CLOUD PRO 2026.

6. **[Software e Licenciamento]** (49203409000102-1-000010/2023)
   - **Objeto:** Contratação de acessos corporativos à plataforma de aprendizagem Alura, conforme condições e exigências estabelecidas neste instrumento.

7. **[Software e Licenciamento]** (46374500000194-1-004039/2025)
   - **Objeto:** Contratação de empresa para aquisição de software para relógio de ponto

8. **[Software e Licenciamento]** (44837524000107-1-000011/2026)
   - **Objeto:** Contratação de pessoa jurídica para a fornecimento e implantação de Sistema de Gestão de Despachos de Guarnições da Guarda Portuária, incluindo licenças de software, dispositivos móveis, análise de placas dos veículos, suporte e treinamento, para atendimento de demandas da Autoridade Portuária de Santos - APS, pelo prazo de 36 (trinta e seis) meses, nos termos e condições estabelecidas no "Termo de Referência" e seus Anexos, partes integrantes deste Edital.

9. **[Software e Licenciamento]** (49203409000102-1-000048/2025)
   - **Objeto:** Contratação de empresa especializada na prestação de serviços em gestão de plataforma digital com foco na saúde e bem-estar, que garanta acesso a estabelecimentos físicos parceiros voltados a atividades físicas, conforme especificações técnicas constantes do Termo de Referência (Anexo I do Edital).

10. **[Software e Licenciamento]** (46374500000194-1-003749/2025)
   - **Objeto:** Aquisição de sistema de chamada de enfermagem.

11. **[Redes, Cloud e Segurança]** (58200015000183-1-000483/2026)
   - **Objeto:** Contratação de empresa para prestação de serviços de manutenção preventiva e corretiva da infraestrutura do datacenter do município de Santos, composta pelos sistemas de climatização, detecção, alarme e combate à incêndio com gás fm200 (SDACI), controle de acesso, circuitos elétricos e gerenciamento (DCIM), incluindo material e suporte local e remoto por meio da disponibilização de central de monitoramento 24 horas com controle de chamados... (descrição completa no Edital).

12. **[Redes, Cloud e Segurança]** (49203409000102-1-000018/2025)
   - **Objeto:** Contratação de serviços de videoconferência em nuvem para realização, gravação e transmissão ao vivo, das sessões Ordinárias, Extraordinárias, Audiências Públicas, Câmaras Jovens, Escola do Legislativo bem como as Sessões Solenes da Câmara Municipal de Santos, sendo estas armazenadas e posteriormente disponibilizadas no site do Órgão, conforme especificações técnicas constantes do Termo de Referência (Anexo I do Edital).

13. **[Redes, Cloud e Segurança]** (46374500000194-1-003984/2024)
   - **Objeto:** Aquisição de cabo de rede

14. **[Redes, Cloud e Segurança]** (46384111000140-1-001325/2024)
   - **Objeto:** Contratação de serviços de telefonia fixa comutada – STFC, nas modalidades fixo-fixo e fixo-móvel, para chamadas locais, interurbanas intraestaduais e interestaduais.

15. **[Redes, Cloud e Segurança]** (08717299000101-1-000047/2024)
   - **Objeto:** O objeto da presente dispensa de licitação é a contratação de empresa especializada para configuração e manutenção corretiva na rede de telefonia e PABX do IPREVSANTOS (cabos, placas, conectores, telefones, inserção e remoção de mensagens, e similares), em regime de preço unitário por diária técnica, somente mão de obra sem cobertura de peças, conforme especificações trazidas no Termo de Referência - Anexo I do Edital.

16. **[Redes, Cloud e Segurança]** (46374500000194-1-001288/2024)
   - **Objeto:** Prestação de serviço de instalação/montagem de equipamento e sistemas de rede de telecomunicação e infraestrutura de telefonia

17. **[Redes, Cloud e Segurança]** (00394502000144-1-004973/2026)
   - **Objeto:** Aquisição de nobreaks para a Divisão de Operações do Navio-Patrulha "Maracanã"

18. **[Redes, Cloud e Segurança]** (58200015000183-1-000308/2024)
   - **Objeto:** Contratação de empresa especializada em prestação de serviços de telecomunicações na modalidade STFC (Serviço Telefônico Fixo Comutado), utilizando terminais analógicos e digitais, códigos especiais tri-dígitos, 0800, com fornecimento de equipamento PABX, tecnologia IP em regime de locação e SCM (Serviço de Comunicação Multimídia) internet Banda Larga/Fibra Ótica, pelo período de 12 (doze) meses, podendo ser prorrogado por sucessivos períodos, até o limite de 60 (sessenta) meses.

19. **[Redes, Cloud e Segurança]** (58158635000100-1-000013/2025)
   - **Objeto:** Contratação de empresa para a prestação de Assinatura de Internet Fibra Banda Larga 300 MBPS ultra velocidade.

20. **[Redes, Cloud e Segurança]** (58200015000183-1-000218/2025)
   - **Objeto:** Seleção de propostas para REGISTRO DE PREÇOS visando a execução de serviços de instalação de fibra ótica, cabeamento estruturado, rede sem fio (wifi) e monitoramento por câmeras IP, para atender as diversas unidades da Prefeitura Municipal de Santos e Instituto de Previdência Social dos Servidores Municipais de Santos, incluindo material e mão de obra, conforme descrição constante no Anexo I – Termo de Referência deste Edital.

21. **[Serviços de TI]** (46377800000127-1-003382/2025)
   - **Objeto:** Contratação de serviços de impressão corporativa por meio de outsourcing de serviços com locação de equipamentos e disponibilização de software de gerenciamento, para o 14ºBPM/I.

22. **[Serviços de TI]** (49203409000102-1-000040/2026)
   - **Objeto:** Contratação de empresa para prestação de serviços de transmissão audiovisual para a Câmara Municipal de Santos, abrangendo planejamento técnico, produção, pósprodução, veiculação e transmissão ao vivo e gravada de eventos legislativos, conforme especificações técnicas constantes do Termo de Referência Anexo I do Edital.

23. **[Serviços de TI]** (15563047000130-1-000008/2025)
   - **Objeto:** [LICITANET] - prestação de serviços de capacitação empreendedora e tecnológica, incluindo a realização de cursos, palestras e mentorias, bem como a execução de ações gratuitas de apoio ao ecossistema de inovação de Santos, pelo período de 12 (doze) meses.

24. **[Serviços de TI]** (58200015000183-1-000312/2025)
   - **Objeto:** Contratação de empresa para prestação de serviços de tratamento de dados, geração de relatórios e demonstrativos para análise técnica e gerencial sobre indicadores de gestão fiscal, avaliação do cumprimento das metas físicas e indicadores dos programas de governo, para a Controladoria Geral da Prefeitura Municipal de Santos, pelo período de 60 (sessenta) meses, conforme descrição constante no Anexo I – Termo de Referência deste Edital.

25. **[Serviços de TI]** (08717299000101-1-000014/2024)
   - **Objeto:** Contratação de serviços especializados em solução de tecnologia da informação para batimento de dados relacionados aos registros de casamentos e óbitos e aos dados do SIRC, disponibilizado pela Empresa de Tecnologia e Informações da Previdência/DATAPREV.

26. **[Serviços de TI]** (01446932000125-1-000042/2024)
   - **Objeto:** Prestação dos serviços de Gestão e Monitoramento de Tecnologia da Informação, pelo período de 12(doze) meses, para as unidades e sede da Fundação Arquivo e Memória de Santos – FAMS, conforme descrito no referido Edital, Termo de Referência e demais Anexos.

27. **[Serviços de TI]** (46377800000127-1-002981/2025)
   - **Objeto:** Serviços de impressão corporativa por meio de outsourcing, na modalidade de locação de equipamentos com disponibilização de software de gerenciamento, inventário, contabilização, manutenção periódica, substituição de equipamentos em casos de quebra e/ou mau funcionamento, fornecimento de suprimentos e sem fornecimento de papel, com vistas a prover o desenvolvimento de atividades de apoio administrativo e operacional no 29º BPM/I

28. **[Serviços de TI]** (08717299000101-1-000030/2026)
   - **Objeto:** Contratação de empresa pública federal especializada na prestação de serviços de processamento de dados e tecnologia da informação para realização de batimento de dados junto ao Sistema de Informações do Registro Civil – SIRC, pelo período de 36 meses.

29. **[Serviços de TI]** (01446932000125-1-000029/2024)
   - **Objeto:** Prestação de serviços de gestão e monitoramento de tecnologia da informação, pelo período de 12 (doze) meses nas unidades da FAMS. devendo incluir:Manutenção dos equipamentos (hardware) da FAMS.

30. **[Serviços de TI]** (44837524000107-1-000014/2026)
   - **Objeto:** Contratação de pessoa jurídica para a prestação dos serviços de atendimento a usuários de Tecnologias da Informação e Comunicação, operação de infraestrutura, incluindo instalações, configurações, manutenções preventivas e corretivas em ativos tecnológicos da Autoridade Portuária de Santos - APS, pelo prazo de 36 (trinta e seis) meses, nos termos e condições estabelecidas no "Termo de Referência" e seus Anexos, partes integrantes deste Edital.

31. **[Hardware e Equipamentos]** (01450928000130-1-000002/2026)
   - **Objeto:** Aquisição de equipamentos de informática (microcomputador completo, pacote de licença Microsoft Windows, pen drive, roteador e HD externo), para serem utilizados pelos funcionários da Fundação Pró-Esportes de Santos – FUPES, conforme descrição constante no Anexo I – Termo de Referência deste Edital.

32. **[Hardware e Equipamentos]** (58200015000183-1-000221/2026)
   - **Objeto:** AQUISIÇÃO DE WEBCAMS FULL HD 1080P, COM CONEXÃO USB E MICROFONE EMBUTIDO, DESTINADAS AO ATENDIMENTO DA SECAFUR (SEÇÃO DE CAPACITAÇÃO DOS FUNCIONÁRIOS DA REDE SOCIOASSISTENCIAL) E DA COAFI (COORDENADORIA ADMINISTRATIVA, DE CONTROLE ORÇAMENTÁRIO, FINANCEIRO

33. **[Hardware e Equipamentos]** (58200015000183-1-000535/2026)
   - **Objeto:** Aquisição de componentes de armazenamento e módulos de memória, necessários à atualização tecnológica dos microcomputadores, da Secretaria Municipal de Finanças e Gestão-SEFIN, do Município de Santos.

34. **[Hardware e Equipamentos]** (58200015000183-1-000737/2025)
   - **Objeto:** Aquisição de Scanner 3D, Máquina de lavar e curar peças de resina e Impressora 3D FDM, a serem utilizados na Unidade Municipal de Ensino - UME dos Andradas II, da Secretaria Municipal de Educação - SEDUC do Município de Santos.

35. **[Hardware e Equipamentos]** (58200015000183-1-000424/2026)
   - **Objeto:** Aquisição de equipamentos de informática (microcomputadores tipo microdesktop, monitores de vídeo e estabilizadores) destinados ao atendimento das necessidades operacionais do Departamento de Políticas e Controle Ambiental (DEPCAM), da Secretaria Municipal de Meio Ambiente, Desenvolvimento Urbano e Sustentabilidade - SEMAM do Município de Santos.

36. **[Hardware e Equipamentos]** (46374500000194-1-008693/2024)
   - **Objeto:** Aquisição de nobreak

37. **[Hardware e Equipamentos]** (58200015000183-1-000278/2024)
   - **Objeto:** Drone Completo para Pulverização (larvicida / inseticida)

38. **[Hardware e Equipamentos]** (58200015000183-1-000512/2024)
   - **Objeto:** Aquisição de Projetor Multimídia, da Secretaria Municipal de Saúde - SMS

39. **[Hardware e Equipamentos]** (00394502000144-1-013981/2024)
   - **Objeto:** Aquisição de servidor de arquivos para o Navio-Patrulha Maracanã

40. **[Hardware e Equipamentos]** (46377800000127-1-000545/2024)
   - **Objeto:** Conserto da impressora patrimônio nº 8043 - 5 DP Santos

41. **[Não-TIC]** (01450928000130-1-000011/2025)
   - **Objeto:** Aquisição bola oficial, para ser utilizada pela equipe de Ginástica Rítmica da Fundação Pró-Esporte de Santos, conforme descrição constante no Anexo I – Termo de Referência do Edital.

42. **[Não-TIC]** (46377800000127-1-002294/2025)
   - **Objeto:** Aquisição de itens de COPA e COZINHA para o efetivo da sede do 6º BPM/I (Santos/SP)

43. **[Não-TIC]** (58200015000183-1-000496/2026)
   - **Objeto:** Contratação para prestação de serviços técnicos de treinamento eaperfeiçoamento de pessoal.

44. **[Não-TIC]** (58200015000183-1-000205/2025)
   - **Objeto:** Aquisição de materiais para reestruturação do Espaço de Brincar da Casinha e Sala de Multilinguagens (ateliê), da UME Maria Patrícia Fogaça, da Secretaria Municipal de Educação - SEDUC, conforme descrição constante no Anexo I – Termo de Referência do Edital.

45. **[Não-TIC]** (58200015000183-1-000035/2026)
   - **Objeto:** Contratação de empresa para prestação de serviço de arbitragem, realizado por staff técnico formado por árbitros e mesários, incluindo o fornecimento de materiais e equipamentos em regime de comodato, destinados ao evento “5º Campeonato Santista de Futevôlei”

46. **[Não-TIC]** (00394460000141-1-001633/2023)
   - **Objeto:** Aquisição de camisetas personalizadas para compor uniforme tático de servidores que atuam na DIREP em operações e ações externas. Em caso de divergências entre as definições do código CATMAT e do Termo de Referência, prevalecerão as especificações do Termo de Referência.

47. **[Não-TIC]** (46377222000129-1-000372/2024)
   - **Objeto:** Aquisição de Lâmpadas de LED, conforme do Aviso de Contratações e seus Anexos.

48. **[Não-TIC]** (58200015000183-1-000689/2024)
   - **Objeto:** Seleção de propostas para REGISTRO DE PREÇOS visando o fornecimento de MEDICAMENTOS, a serem utilizados pela Secretaria Municipal de Saúde – SMS

49. **[Não-TIC]** (58200015000183-1-000463/2026)
   - **Objeto:** CREDENCIAMENTO de empresas especializadas na administração, gerenciamento, emissão, distribuição e fornecimento de cartão de vale-alimentação eletrônico, magnético ou de similar tecnologia, conforme descrição constante no Anexo I – Termo de Referência deste Edital.

50. **[Não-TIC]** (46377800000127-1-001501/2025)
   - **Objeto:** Contratação de empresa especializada para execução de serviço de manutenção preventiva e corretiva, com aplicação de reposição de peças originais e/ou genuínas em embarcação pertencente ao 2º BAEP
