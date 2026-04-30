# Guia de Figuras, Tabelas e Arquivos — Frente Python

## 1. Objetivo deste guia

Este documento organiza, de forma direta, quais arquivos sustentam cada parte do texto da frente Python. Ele também indica em que momento cada figura deve ser citada no capítulo de resultados.

## 2. Arquivos numéricos centrais

### 2.1 Experimentos principais
- `comparison_table_experiments_main.csv`
- `all_runs_experiments_main.csv`

### 2.2 Sensibilidade
- `comparison_table_experiments_sensitivity.csv`
- `all_runs_experiments_sensitivity.csv`

### 2.3 PPO por versão
- `rl_eval_summary_ppo_both_v1.csv`
- `rl_eval_summary_ppo_v2_both.csv`
- `rl_eval_summary_ppo_v3_both.csv`
- `rl_eval_summary_ppo_v4_both.csv`
- `rl_eval_runs_ppo_v1_both.csv`
- `rl_eval_runs_ppo_v2_both.csv`
- `rl_eval_runs_ppo_v3_both.csv`
- `rl_eval_runs_ppo_v4_both.csv`

### 2.4 Robustez PPO v4
- `rl_robustness_summary_ppo_v4_both.csv`
- `rl_robustness_runs.csv`
- `robustness_rl_vs_heuristics_robustness_ppo_v4.csv`

## 3. Tabelas consolidadas desta revisão

### Tabela 1 — heurísticas em `baseline_both`
Arquivo: `tables/table_01_main_baseline_both_heuristics.csv`

| Heurística          |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |   Fairness final |   Fila final |
|:--------------------|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|-----------------:|-------------:|
| proportional_fair   |                157.628 |            0.772 |             0.823 |           0.21  |                     15.336 |            0.819 |         61.3 |
| round_robin         |                152.475 |            0.779 |             0.817 |           0.203 |                     14.323 |            0.963 |         60.1 |
| longest_queue_first |                153.061 |            0.778 |             0.819 |           0.204 |                     14.674 |            0.937 |         60.1 |
| greedy_backlog      |                192.094 |            0.725 |             0.838 |           0.252 |                     15.56  |            0.985 |         62.4 |

### Tabela 2 — sensibilidade com `proportional_fair`
Arquivo: `tables/table_02_sensitivity_proportional_fair.csv`

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

### Tabela 3 — evolução das versões PPO
Arquivo: `tables/table_03_rl_versions_summary.csv`

| Versão PPO   |   Recompensa média |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |
|:-------------|-------------------:|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|
| ppo_v1       |             -0.504 |                153.171 |            0.779 |             0.817 |           0.202 |                     14.208 |
| ppo_v2       |              4.388 |                155.804 |            0.778 |             0.821 |           0.205 |                     14.051 |
| ppo_v3       |             74.362 |                156.229 |            0.777 |             0.821 |           0.206 |                     14.127 |
| ppo_v4       |             77.459 |                159.496 |            0.772 |             0.823 |           0.211 |                     14.042 |

### Tabela 4 — comparação final entre PPO v4 e heurísticas
Arquivo: `tables/table_04_final_rl_v4_vs_heuristics.csv`

| Estratégia          |   Goodput médio (Mbps) |   Bloqueio final |   Aceitação média |   Serviço médio |   Atraso servido final (s) |   Fairness final |   Fila final |
|:--------------------|-----------------------:|-----------------:|------------------:|----------------:|---------------------------:|-----------------:|-------------:|
| proportional_fair   |                157.628 |            0.772 |             0.823 |           0.21  |                     15.336 |            0.819 |         61.3 |
| round_robin         |                152.475 |            0.779 |             0.817 |           0.203 |                     14.323 |            0.963 |         60.1 |
| longest_queue_first |                153.061 |            0.778 |             0.819 |           0.204 |                     14.674 |            0.937 |         60.1 |
| greedy_backlog      |                192.094 |            0.725 |             0.838 |           0.252 |                     15.56  |            0.985 |         62.4 |
| ppo_v4              |                159.496 |            0.772 |             0.823 |           0.211 |                     14.042 |            0.691 |         60.4 |

### Tabela 5 — robustez do PPO v4
Arquivo: `tables/table_05_rl_v4_robustness_summary.csv`

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

## 4. Figuras corretas e onde entram no texto

### Bloco: comparação de heurísticas no cenário principal
- **Figura 1**: `images/fig_01_baseline_both_goodput.png`
- **Figura 2**: `images/fig_02_baseline_both_blocking.png`
- **Figura 3**: `images/fig_03_baseline_both_delay.png`

### Bloco: evolução do PPO
- **Figura 4**: `images/fig_04_rl_versions_goodput.png`
- **Figura 5**: `images/fig_05_rl_versions_reward.png`
- **Figura 6**: `images/fig_10_boxplot_rl_versions_goodput.png`
- **Figura 7**: `images/fig_11_boxplot_rl_versions_reward.png`

### Bloco: sensibilidade com `proportional_fair`
- **Figura 8**: `images/fig_06_sensitivity_pf_goodput.png`
- **Figura 9**: `images/fig_07_sensitivity_pf_blocking.png`

### Bloco: robustez da PPO v4
- **Figura 10**: `images/fig_08_rl_v4_robustness_goodput.png`
- **Figura 11**: `images/fig_09_rl_v4_robustness_blocking.png`
- **Figura 12**: `images/fig_12_boxplot_rl_v4_robustness_goodput.png`

## 5. Verificação de consistência entre tabelas e figuras

A revisão atual confirmou o alinhamento entre os CSVs e as figuras fornecidas:

- as barras de goodput do cenário `baseline_both` seguem a Tabela 4;
- a evolução do goodput entre `ppo_v1` e `ppo_v4` segue a Tabela 3;
- a sensibilidade com `proportional_fair` segue a Tabela 2;
- a robustez da PPO v4 segue a Tabela 5.

Portanto, as imagens desta revisão podem ser utilizadas como base visual correta da frente Python.

## 6. Observação sobre rascunhos textuais antigos

Rascunhos textuais anteriores, como `Texto colado.txt`, `Texto colado (2).txt` e `Texto colado (3).txt`, serviram como apoio de redação, mas não devem mais ser tratados como base numérica final. A base definitiva desta revisão é a formada pelos CSVs listados neste documento.
