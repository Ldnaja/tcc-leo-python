# Sistema Desenvolvido — Frente Python

## 1. Visão geral da frente Python

A frente Python foi desenvolvida como o ambiente principal de investigação do problema de alocação dinâmica de canais em redes LEO multifeixe sob carga variável. Seu papel central no trabalho foi permitir a modelagem controlada do sistema, a comparação entre heurísticas clássicas de alocação e a integração progressiva de um agente de aprendizado por reforço.

A escolha por uma frente própria em Python teve três objetivos principais. O primeiro foi permitir controle direto sobre as abstrações do problema, tornando viável ajustar carga, número de canais, nível de interferência, política de alocação e mecanismos de congestionamento. O segundo foi criar uma infraestrutura suficientemente flexível para testar rapidamente múltiplos cenários e gerar bases comparativas repetíveis com várias seeds. O terceiro foi fornecer um ambiente compatível com integração direta com bibliotecas de aprendizado por reforço, sem depender inicialmente de um simulador de rede mais pesado.

Assim, a frente Python não foi tratada como um substituto de ferramentas de rede em nível de pacote, mas como o núcleo analítico do TCC para estudar a lógica de decisão e o impacto da redistribuição de canais em um ambiente LEO multifeixe simplificado.

## 2. Objetivo técnico do sistema

O sistema foi projetado para responder, em ambiente controlado, a uma pergunta central: como diferentes políticas de alocação de canais se comportam quando a carga de tráfego varia ao longo do tempo e se concentra espacialmente em determinadas regiões da cobertura?

Para responder a essa questão, o simulador foi estruturado para representar:

- uma topologia multifeixe com 19 beams;
- uma carga variável no tempo;
- uma região de hotspot com pressão localizada de demanda;
- uma quantidade total limitada de canais;
- um limite de canais por beam;
- degradação de enlace por perda de qualidade espacial e interferência simplificada;
- filas por beam;
- bloqueio por fila máxima;
- descarte por timeout;
- avaliação por múltiplas métricas operacionais;
- comparação entre heurísticas e PPO.

## 3. Arquitetura lógica do simulador

A arquitetura foi organizada de forma modular para separar geração de tráfego, modelagem de enlace, alocação de recursos, coleta de métricas e integração com RL.

Em linhas gerais, o fluxo do simulador segue a sequência abaixo:

1. a topologia hexagonal dos beams é inicializada;
2. o gerador de tráfego cria novas requisições a cada passo de tempo;
3. o sistema aplica filtros de congestionamento, como fila máxima e timeout;
4. a política de alocação distribui os canais disponíveis entre os beams ativos;
5. a qualidade de enlace de cada beam é estimada com base na posição relativa ao hotspot e na interferência dos vizinhos;
6. a vazão instantânea de cada beam é calculada a partir da eficiência espectral;
7. as requisições nas filas são atendidas de acordo com a capacidade disponível no passo;
8. as métricas acumuladas e por passo são atualizadas.

Essa organização permitiu reusar a mesma infraestrutura tanto para os experimentos com heurísticas quanto para os episódios de treinamento e avaliação do agente PPO.

## 4. Organização em módulos

### 4.1 Núcleo estrutural

O núcleo estrutural concentra entidades e topologia. Nesse bloco ficam os estados dos beams, as requisições de usuários e a construção da malha hexagonal com relação de vizinhança.

### 4.2 Geração de tráfego

A geração de tráfego foi separada em um módulo próprio para permitir controlar taxa base de chegadas, intensidade do hotspot, período temporal de variação e demanda média de serviço por requisição.

### 4.3 Modelo de canal

O modelo de canal calcula a qualidade lógica do enlace por beam. Esse cálculo considera um valor base de SNR, uma penalização espacial associada à distância relativa ao hotspot e uma penalização adicional de interferência em função da ocupação dos beams vizinhos. Em seguida, a eficiência espectral é usada para converter a condição de enlace em throughput efetivo.

### 4.4 Alocação de recursos

A camada de alocação recebe o estado das filas e distribui os canais disponíveis de acordo com a política selecionada. Nessa camada foram implementadas as heurísticas `proportional_fair`, `round_robin`, `longest_queue_first` e `greedy_backlog`, além da interface que recebe ações externas do agente PPO.

### 4.5 Métricas e resultados

A coleta de métricas foi centralizada para padronizar tanto os experimentos com heurísticas quanto a avaliação do PPO. Essa escolha garantiu comparabilidade direta entre os métodos.

## 5. Modelo abstrato adotado

O simulador não busca reproduzir integralmente a física orbital e todos os detalhes de uma rede NTN operacional. O foco foi uma representação controlada do problema de alocação dinâmica de canais, com abstrações suficientes para manter coerência técnica e, ao mesmo tempo, viabilidade experimental.

As principais abstrações adotadas foram:

- topologia multifeixe fixa de 19 beams, em vez de uma constelação orbital completa;
- hotspot lógico para representar assimetria espacial de carga;
- qualidade de enlace simplificada por SNR e penalidade de interferência;
- canal compartilhado modelado como conjunto finito de recursos discretos;
- atendimento de tráfego em nível de requisição agregada, e não em nível de pacote;
- congestão observada por filas, bloqueio e timeout, em vez de protocolos completos de rede.

Essas abstrações foram escolhidas para manter o problema diretamente alinhado ao objetivo do TCC: estudar a redistribuição dinâmica de canais sob pressão de carga.



### 5.1 Fundamentação metodológica das abstrações

A construção do simulador não partiu da reprodução literal de um único artigo ou de um stack industrial fechado. A estratégia adotada foi combinar elementos recorrentes da literatura de redes NTN/LEO e de alocação dinâmica de recursos com simplificações controladas adequadas ao objetivo do TCC.

Em termos metodológicos, a modelagem se apoia em cinco ideias amplamente aceitas na literatura:

- uso de cobertura multifeixe como estrutura natural de distribuição espacial do tráfego;
- existência de assimetria espacial de carga, representada aqui por hotspot;
- limitação finita de recursos de rádio, abstraída como um pool total de canais;
- degradação do atendimento sob saturação, observada por filas, bloqueio e atraso;
- comparação entre políticas fixas e políticas adaptativas orientadas por estado.

Assim, a frente Python deve ser entendida como um simulador experimental **inspirado por princípios reais de redes multifeixe**, mas propositalmente simplificado para análise de decisão. Em outras palavras, ele não pretende ser um gêmeo digital orbital completo, e sim um ambiente de estudo cientificamente defensável para o problema específico de redistribuição dinâmica de canais.


## 6. Parâmetros principais utilizados

A configuração principal da frente Python, usada como referência no cenário `baseline_both`, foi:

- `n_beams = 19`;
- `total_channels = 48`;
- `max_channels_per_beam = 6`;
- `total_power_w = 120.0`;
- `duration_s = 600`;
- `dt_s = 1.0`;
- `base_arrival_rate = 0.18`;
- `hotspot_amplitude = 0.70`;
- `hotspot_period_s = 180`;
- `mean_service_demand_mb = 24`;
- `base_snr_db = 18.0`;
- `edge_loss_db = 6.0`;
- `interference_penalty_db = 4.5`;
- `channel_bandwidth_hz = 1e6`;
- `max_queue_per_beam = 5`;
- `max_wait_s = 20.0`.

Essa parametrização foi importante porque criou um regime de saturação controlada: o sistema não opera em folga total, mas também não entra em colapso trivial. Isso permitiu diferenciar de forma clara as políticas de alocação.

## 7. Heurísticas implementadas

As heurísticas clássicas foram inseridas para fornecer uma base comparativa forte antes da etapa de RL.

- **Round Robin** distribui recursos de forma rotativa, com baixa sensibilidade à pressão instantânea de carga.
- **Longest Queue First** prioriza beams com maior fila acumulada, buscando aliviar backlog.
- **Proportional Fair** tenta equilibrar pressão de demanda e distribuição relativamente justa dos recursos.
- **Greedy Backlog** prioriza de forma mais agressiva os beams mais pressionados, com foco maior em throughput total.

Essas políticas não foram incluídas apenas como baseline trivial. Elas constituem o referencial principal contra o qual o PPO foi avaliado.

## 8. Métricas monitoradas

As métricas monitoradas na frente Python foram:

- carga oferecida média;
- carga aceita média;
- capacidade média alocada;
- goodput médio;
- fila média e fila final;
- taxa final de bloqueio;
- taxa final de bloqueio por fila máxima;
- taxa final de bloqueio por timeout;
- taxa média de aceitação;
- taxa média de serviço;
- atraso médio final de requisições servidas;
- atraso P95 final;
- fairness de Jain;
- utilização dos canais.

A seleção dessas métricas foi importante porque permitiu analisar não apenas throughput, mas também custo operacional da decisão. Dessa forma, uma política não é julgada apenas por transportar mais dados, mas também por seu efeito sobre bloqueio, atraso, equilíbrio e acúmulo de fila.

## 9. Integração com aprendizado por reforço

Após a consolidação das heurísticas, a mesma base do simulador foi conectada a uma interface compatível com `gymnasium`, permitindo o treinamento de um agente PPO por meio de `stable-baselines3`.

Nessa integração:

- o **estado** do ambiente passa a representar, de forma normalizada, o estado das filas, canais alocados, SINR, throughput por beam e indicadores globais;
- a **ação** do agente é um vetor contínuo de prioridades por beam;
- essa ação é convertida em distribuição discreta de canais pela função de alocação baseada em prioridade;
- a **recompensa** combina goodput, bloqueio, fila, atraso e fairness.

A integração foi feita sobre o mesmo simulador-base, o que preserva a comparabilidade metodológica com as heurísticas.

## 10. Saídas produzidas pelo sistema

A frente Python gera saídas em formatos adequados tanto para análise exploratória quanto para redação do TCC:

- `history.csv` por execução;
- `summary.json` por execução;
- tabelas consolidadas `comparison_table.csv`;
- arquivos `all_runs.csv` com todas as seeds;
- figuras por métrica;
- resumos de avaliação do PPO;
- comparações entre PPO e heurísticas;
- comparações de robustez.

Essa estrutura foi fundamental para permitir uma trilha metodológica reproduzível.

## 11. Papel da frente Python no trabalho

No contexto do TCC, a frente Python deve ser apresentada como o sistema principal desenvolvido para estudar a alocação dinâmica de canais em redes LEO multifeixe sob carga variável.

É nessa frente que foram consolidados:

- o problema experimental;
- os cenários principais;
- a comparação entre heurísticas;
- a análise de sensibilidade;
- a integração com PPO;
- a avaliação de robustez do agente treinado.

A frente NS-3, a ser inserida posteriormente, pode ser tratada como ambiente complementar de verificação em nível de rede. Assim, as duas frentes convergem para a mesma ideia: uma serve para estudar e comparar a lógica de decisão com maior controle experimental, e a outra serve para observar a manifestação dessa decisão em um ambiente de rede mais próximo de transmissão efetiva.
