# Resultados e Análise — Frente Python

## 1. Base revisada desta análise

Esta análise foi revisada com base nos CSVs consolidados e nas figuras finais geradas a partir deles. Os arquivos centrais usados nesta etapa foram:

- `tables/table_01_main_baseline_both_heuristics.csv`
- `tables/table_02_sensitivity_proportional_fair.csv`
- `tables/table_03_rl_versions_summary.csv`
- `tables/table_04_final_rl_v4_vs_heuristics.csv`
- `tables/table_05_rl_v4_robustness_summary.csv`
- `tables/table_06_rl_v4_robustness_vs_heuristics.csv`

Além deles, foram usados como apoio:

- `comparison_table_experiments_main.csv`
- `comparison_table_experiments_sensitivity.csv`
- `rl_eval_summary_ppo_both_v1.csv`
- `rl_eval_summary_ppo_v2_both.csv`
- `rl_eval_summary_ppo_v3_both.csv`
- `rl_eval_summary_ppo_v4_both.csv`
- `rl_robustness_summary_ppo_v4_both.csv`
- `robustness_rl_vs_heuristics_robustness_ppo_v4.csv`

## 2. Leitura geral dos experimentos principais

Os experimentos principais foram estruturados em quatro cenários-base:

- `baseline`: sem saturação relevante;
- `baseline_queue_cap`: com limitação explícita de fila;
- `baseline_timeout`: com descarte por timeout;
- `baseline_both`: com fila máxima e timeout combinados.

A Tabela 1 resume, para cada cenário, a estratégia com maior goodput médio.

### Tabela 1 — Melhor estratégia por cenário-base
| Cenário            | Melhor estratégia por goodput   |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |
|:-------------------|:--------------------------------|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|
| baseline           | greedy_backlog                  |                 40.849 |            0     |             0.999 |           0.984 |                      2.539 |
| baseline_both      | greedy_backlog                  |                192.094 |            0.725 |             0.838 |           0.252 |                     15.56  |
| baseline_queue_cap | greedy_backlog                  |                190.19  |            0.122 |             0.989 |           0.251 |                    217.334 |
| baseline_timeout   | greedy_backlog                  |                192.644 |            0.72  |             1     |           0.251 |                     16.378 |

A leitura inicial dessa tabela mostra um comportamento importante. No cenário `baseline`, todas as heurísticas convergem para resultados praticamente idênticos, indicando que não há pressão suficiente para diferenciar políticas. Já nos cenários com saturação, `greedy_backlog` aparece como a estratégia de maior goodput, o que confirma que políticas agressivas de priorização de backlog conseguem empurrar mais tráfego quando o sistema opera sob forte pressão.

No entanto, goodput não foi a única dimensão considerada. Por isso, a análise detalhada do TCC concentrou-se no cenário `baseline_both`, que foi adotado como cenário principal por combinar simultaneamente fila máxima e timeout.

## 3. Comparação das heurísticas no cenário principal `baseline_both`

A Tabela 2 consolida os resultados das heurísticas no cenário `baseline_both`.

### Tabela 2 — Heurísticas no cenário `baseline_both`
| Heurística          |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |   Fairness final |   Fila final |
|:--------------------|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|-----------------:|-------------:|
| proportional_fair   |                157.628 |            0.772 |             0.823 |           0.21  |                     15.336 |            0.819 |         61.3 |
| round_robin         |                152.475 |            0.779 |             0.817 |           0.203 |                     14.323 |            0.963 |         60.1 |
| longest_queue_first |                153.061 |            0.778 |             0.819 |           0.204 |                     14.674 |            0.937 |         60.1 |
| greedy_backlog      |                192.094 |            0.725 |             0.838 |           0.252 |                     15.56  |            0.985 |         62.4 |

A leitura da Tabela 2 mostra que `greedy_backlog` foi a política de maior goodput médio, alcançando **192.094 Mbps**, com menor bloqueio final (**0.725**) e maior taxa média de serviço (**0.252**) entre as heurísticas avaliadas. Isso confirma o caráter agressivo da política, que privilegia beams mais pressionados e, com isso, maximiza o volume de tráfego efetivamente atendido.

Por outro lado, as heurísticas intermediárias ficaram concentradas em uma faixa bastante próxima, entre **152 e 158 Mbps** de goodput médio. Nessa faixa, `proportional_fair` se destacou como a melhor heurística equilibrada, com **157.628 Mbps**, superando `round_robin` e `longest_queue_first` em goodput e taxa de serviço.

As Figuras 1, 2 e 3 devem ser inseridas nesta parte do texto.

- **Figura 1** — `images/fig_01_baseline_both_goodput.png`
- **Figura 2** — `images/fig_02_baseline_both_blocking.png`
- **Figura 3** — `images/fig_03_baseline_both_delay.png`

A Figura 1 reforça visualmente a diferença entre `greedy_backlog` e o grupo intermediário. A Figura 2 mostra que esse maior goodput veio acompanhado de menor bloqueio final. Já a Figura 3 deixa claro que a política agressiva não foi a melhor em atraso servido final: nesse critério, `round_robin` e depois `longest_queue_first` ficaram abaixo de `greedy_backlog`.

Essa combinação de resultados é importante porque justifica a divisão interpretativa feita ao longo do trabalho:

- `greedy_backlog` foi a melhor política de **maximização de atendimento**;
- `proportional_fair` foi a melhor heurística de **referência balanceada**;
- `round_robin` e `longest_queue_first` funcionaram como políticas intermediárias de comparação.

## 4. Sensibilidade do cenário principal

A análise de sensibilidade foi conduzida a partir de variações em:

- número total de canais;
- penalidade de interferência;
- combinação entre fila máxima e timeout.

Como referência, a leitura principal foi feita sobre a heurística `proportional_fair`, já que ela representou a baseline balanceada do trabalho.

### Tabela 3 — Sensibilidade com `proportional_fair`
| Cenário      |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |
|:-------------|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|
| both_ch32    |                106.565 |            0.84  |             0.814 |           0.14  |                     15.576 |
| both_ch64    |                205.125 |            0.713 |             0.832 |           0.27  |                     14.951 |
| both_int3    |                177.466 |            0.747 |             0.827 |           0.235 |                     15.233 |
| both_int6    |                138.453 |            0.798 |             0.82  |           0.183 |                     15.409 |
| both_q5_t10  |                162.3   |            0.781 |             0.967 |           0.211 |                      7.332 |
| both_q5_t40  |                152.222 |            0.772 |             0.592 |           0.205 |                     30.113 |
| both_q10_t20 |                159.252 |            0.767 |             0.994 |           0.207 |                     16.157 |
| both_q15_t20 |                159.308 |            0.767 |             1     |           0.207 |                     16.187 |

As Figuras 4 e 5 desta seção devem ser:

- **Figura 4** — `images/fig_06_sensitivity_pf_goodput.png`
- **Figura 5** — `images/fig_07_sensitivity_pf_blocking.png`

A análise da Tabela 3 e das Figuras 4 e 5 leva a quatro conclusões centrais.

### 4.1 Efeito do número de canais

A redução para `both_ch32` derrubou o goodput médio para **106.565 Mbps** e elevou o bloqueio final para **0.840**. Em sentido oposto, a expansão para `both_ch64` elevou o goodput para **205.125 Mbps** e reduziu o bloqueio final para **0.713**. Isso mostra que a disponibilidade total de canais é o parâmetro mais sensível do conjunto avaliado.

### 4.2 Efeito da interferência

Quando a penalidade de interferência foi reduzida para `both_int3`, o goodput subiu para **177.466 Mbps**. Quando a penalidade foi elevada para `both_int6`, o goodput caiu para **138.453 Mbps**. Isso indica que o modelo responde corretamente à deterioração das condições de enlace.

### 4.3 Efeito do timeout

A configuração `both_q5_t10` reduziu o atraso servido final para **7.332 s**, com aceitação média ainda alta (**0.967**), ao custo de manter um bloqueio final relativamente elevado (**0.781**). Em contrapartida, `both_q5_t40` elevou o atraso final para **30.113 s** e derrubou a aceitação média para **0.592**. Isso evidencia o custo operacional de permitir que requisições aguardem por muito mais tempo sob saturação.

### 4.4 Efeito da fila máxima

Os casos `both_q10_t20` e `both_q15_t20` elevaram a aceitação média para valores próximos de **1.0**, mas não produziram ganho relevante de goodput em relação ao cenário principal. Isso mostra que aumentar a fila máxima melhora a admissão lógica de requisições, mas não altera de forma estrutural a capacidade efetiva do sistema.

## 5. Evolução do PPO entre versões

A integração com RL foi feita por etapas, produzindo quatro versões de PPO. A Tabela 4 resume essa evolução.

### Tabela 4 — Evolução das versões PPO
| Versão PPO   |   Recompensa média |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |
|:-------------|-------------------:|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|
| ppo_v1       |             -0.504 |                153.171 |            0.779 |             0.817 |           0.202 |                     14.208 |
| ppo_v2       |              4.388 |                155.804 |            0.778 |             0.821 |           0.205 |                     14.051 |
| ppo_v3       |             74.362 |                156.229 |            0.777 |             0.821 |           0.206 |                     14.127 |
| ppo_v4       |             77.459 |                159.496 |            0.772 |             0.823 |           0.211 |                     14.042 |

As Figuras 6, 7, 8 e 9 devem ser inseridas nesta parte.

- **Figura 6** — `images/fig_04_rl_versions_goodput.png`
- **Figura 7** — `images/fig_05_rl_versions_reward.png`
- **Figura 8** — `images/fig_10_boxplot_rl_versions_goodput.png`
- **Figura 9** — `images/fig_11_boxplot_rl_versions_reward.png`

A Tabela 4 e as Figuras 6–9 mostram que o PPO evoluiu de forma consistente ao longo das versões. O goodput médio passou de **153.171 Mbps** na `ppo_v1` para **159.496 Mbps** na `ppo_v4`. Em paralelo, a recompensa média por episódio subiu de **-0.504** para **77.459**, evidenciando melhor alinhamento entre política aprendida e função de recompensa.

A análise das versões permite separar dois movimentos:

1. um ganho moderado, porém contínuo, nas métricas operacionais do ambiente;
2. um ganho mais expressivo na coerência do processo de treinamento, visível pela recompensa média.

Isso explica por que a recompensa melhorou muito mais do que o goodput: parte da melhoria veio da estabilização do comportamento do agente e da melhor adequação entre reward e objetivo de controle.

Os boxplots também confirmam que a `ppo_v4` não apenas teve maior média, mas operou em um patamar superior de seeds, com dispersão ainda controlada.

## 6. Comparação final: PPO v4 versus heurísticas no cenário principal

A Tabela 5 consolida a comparação final entre a `ppo_v4` e as heurísticas no cenário `baseline_both`.

### Tabela 5 — Comparação final no cenário `baseline_both`
| Estratégia          |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |   Fairness final |   Fila final |
|:--------------------|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|-----------------:|-------------:|
| proportional_fair   |                157.628 |            0.772 |             0.823 |           0.21  |                     15.336 |            0.819 |         61.3 |
| round_robin         |                152.475 |            0.779 |             0.817 |           0.203 |                     14.323 |            0.963 |         60.1 |
| longest_queue_first |                153.061 |            0.778 |             0.819 |           0.204 |                     14.674 |            0.937 |         60.1 |
| greedy_backlog      |                192.094 |            0.725 |             0.838 |           0.252 |                     15.56  |            0.985 |         62.4 |
| ppo_v4              |                159.496 |            0.772 |             0.823 |           0.211 |                     14.042 |            0.691 |         60.4 |

A interpretação dessa tabela é central para a conclusão da frente Python.

A `ppo_v4` alcançou **159.496 Mbps** de goodput médio. Com isso, ela:

- superou `proportional_fair` em aproximadamente **1.868 Mbps**;
- superou `longest_queue_first` em aproximadamente **6.435 Mbps**;
- superou `round_robin` em aproximadamente **7.021 Mbps**;
- permaneceu abaixo de `greedy_backlog` em aproximadamente **32.598 Mbps**.

Ao mesmo tempo, a `ppo_v4` obteve atraso servido final de **14.042 s**, menor que o de todas as heurísticas comparadas, inclusive `greedy_backlog`. Isso significa que o agente aprendeu uma política que melhora o grupo intermediário sem reproduzir o comportamento mais agressivo da heuristic greedy.

Do ponto de vista do TCC, essa é a leitura mais importante da frente Python: o agente PPO não ultrapassou a política mais agressiva em throughput bruto, mas conseguiu se posicionar acima das heurísticas intermediárias e, simultaneamente, reduzir atraso. Em outras palavras, a RL mostrou capacidade de produzir uma política competitiva e operacionalmente mais equilibrada.

## 7. Robustez da PPO v4

A análise final de robustez testou a `ppo_v4` nos mesmos cenários de sensibilidade já usados nas heurísticas.

### Tabela 6 — Robustez da `ppo_v4`
| Cenário      |   Recompensa média |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |
|:-------------|-------------------:|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|
| both_ch32    |           -100.649 |                107.447 |            0.841 |             0.812 |           0.14  |                     14.409 |
| both_ch64    |            265.502 |                210.941 |            0.704 |             0.832 |           0.278 |                     13.708 |
| both_int3    |            149.148 |                179.874 |            0.747 |             0.826 |           0.236 |                     13.916 |
| both_int6    |              7.487 |                139.648 |            0.797 |             0.819 |           0.187 |                     14.248 |
| both_q5_t10  |            132.916 |                165.541 |            0.775 |             0.966 |           0.218 |                      6.759 |
| both_q5_t40  |             24.707 |                153.655 |            0.773 |             0.596 |           0.204 |                     27.355 |
| both_q10_t20 |             70.114 |                159.101 |            0.769 |             0.994 |           0.208 |                     14.797 |
| both_q15_t20 |             69.749 |                159.097 |            0.769 |             1     |           0.207 |                     14.815 |

As Figuras 10, 11 e 12 devem ser inseridas nesta parte.

- **Figura 10** — `images/fig_08_rl_v4_robustness_goodput.png`
- **Figura 11** — `images/fig_09_rl_v4_robustness_blocking.png`
- **Figura 12** — `images/fig_12_boxplot_rl_v4_robustness_goodput.png`

A robustez confirma o padrão já observado nas heurísticas. A `ppo_v4` respondeu de forma coerente às mudanças do ambiente:

- pior desempenho em `both_ch32`, com **107.447 Mbps**;
- melhor desempenho em `both_ch64`, com **210.941 Mbps**;
- melhoria em interferência reduzida (`both_int3`);
- degradação em interferência elevada (`both_int6`);
- atraso muito baixo em `both_q5_t10`;
- atraso muito alto em `both_q5_t40`.

Esse comportamento é desejável, porque indica que o agente não aprendeu apenas a memorizar um caso, mas reagiu consistentemente às mudanças de regime do sistema.

Além disso, a comparação direta com `proportional_fair` nos cenários de robustez mostra um resultado importante: a `ppo_v4` apresentou **goodput superior em 6 dos 8 cenários** e **atraso servido final menor em todos os 8 cenários**. As exceções em goodput foram `both_q10_t20` e `both_q15_t20`, nas quais a diferença foi pequena e desfavorável ao PPO.

## 8. Síntese interpretativa da frente Python

A partir da revisão dos CSVs e das figuras corretas, a síntese da frente Python pode ser apresentada em quatro pontos.

### 8.1 O simulador distinguiu corretamente regimes de operação

No cenário sem saturação, as políticas ficaram praticamente equivalentes. Nos cenários pressionados, as diferenças surgiram de forma clara. Isso indica que o ambiente foi bem calibrado para o problema estudado.

### 8.2 As heurísticas produziram uma fronteira clara de comparação

`Greedy_backlog` foi a melhor política em throughput bruto. `Proportional_fair` foi a baseline balanceada. `Round_robin` e `longest_queue_first` serviram como comparadores intermediários.

### 8.3 O PPO evoluiu de modo consistente

A transição entre `ppo_v1` e `ppo_v4` mostrou ganho contínuo em goodput e forte ganho em recompensa média. Isso confirma que houve aprendizado útil, e não apenas variação aleatória entre seeds.

### 8.4 A PPO v4 foi competitiva e robusta

A `ppo_v4` não superou a heuristic mais agressiva, mas conseguiu superar o bloco intermediário de heurísticas, reduzir atraso e manter robustez nos testes de sensibilidade. Portanto, ela se mostrou tecnicamente válida como política adaptativa aprendida para a frente Python.

## 9. Conclusão desta etapa

Os resultados da frente Python são suficientes para sustentar a primeira parte experimental do trabalho. Eles mostram que:

- a modelagem escolhida foi capaz de diferenciar políticas de alocação;
- as heurísticas estabeleceram um referencial comparativo sólido;
- a sensibilidade confirmou coerência estrutural do simulador;
- a RL apresentou ganho real sobre heurísticas intermediárias;
- a versão final `ppo_v4` se manteve estável em testes de robustez.

Assim, a frente Python já fornece um bloco consistente para os capítulos de sistema desenvolvido, resultados e análise de resultados do TCC.
