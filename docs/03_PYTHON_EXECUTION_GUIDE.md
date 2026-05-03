# Guia de Execução — Frente Python do TCC LEO

Este documento explica, passo a passo, como instalar, configurar e executar a frente Python do TCC. O objetivo é deixar a execução reproduzível, desde os cenários base com heurísticas até os experimentos com PPO e os testes de robustez.

## 1. Objetivo deste guia

A frente Python foi usada como ambiente principal de estudo da alocação dinâmica de canais em rede LEO multifeixe simplificada. Nela foram executadas três linhas principais de experimentação:

- comparação entre heurísticas de alocação;
- análise de sensibilidade dos parâmetros mais relevantes;
- treinamento, avaliação e robustez de um agente PPO.

## 2. Organização geral do projeto

A estrutura lógica da frente Python pode ser entendida assim:

```text
tcc-leo-python/
├── configs/
│   ├── baseline.yaml
│   ├── baseline_queue_cap.yaml
│   ├── baseline_timeout.yaml
│   ├── baseline_both.yaml
│   ├── sensitivity/
│   └── rl/
├── scripts/
├── src/
│   ├── allocation/
│   ├── channel/
│   ├── core/
│   ├── metrics/
│   ├── rl/
│   ├── scenarios/
│   └── traffic/
├── results/
└── tests/
```

## 3. Função das principais pastas

### 3.1 `src/`
Contém o código-fonte do simulador.

- `src/scenarios/`: cenários, com destaque para `baseline.py`;
- `src/traffic/`: geração de tráfego;
- `src/channel/`: modelo de canal;
- `src/allocation/`: heurísticas;
- `src/metrics/`: coleta de métricas;
- `src/core/`: entidades e topologia.

### 3.2 RL

- `src/rl/envs/`: ambiente Gymnasium;
- `src/rl/actions/`: conversão de ação contínua em prioridades por beam;
- `src/rl/rewards/`: função de recompensa.

### 3.3 Scripts

- `scripts/run_baseline.py`: execução unitária;
- `scripts/run_experiments.py`: múltiplas seeds, cenários e heurísticas;
- `scripts/train_rl.py`: treinamento PPO;
- `scripts/evaluate_rl.py`: avaliação PPO;
- `scripts/compare_rl_vs_heuristics.py`: comparação PPO versus heurísticas;
- scripts de robustez e consolidação, quando presentes no projeto.

### 3.4 `results/`
Recebe os arquivos gerados:

- históricos por execução;
- figuras;
- tabelas consolidadas;
- checkpoints e avaliações do PPO.

## 4. Ambiente recomendado

O ambiente usado como referência foi:

- Ubuntu 24.04 LTS;
- Python 3.12;
- execução principal em CPU para PPO com política MLP.

Foi utilizada uma `venv` no Ubuntu. O fluxo típico é:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

## 5. Bibliotecas principais

As bibliotecas principais são:

- `pyyaml`
- `numpy`
- `pandas`
- `matplotlib`
- `rich`
- `tqdm`
- `gymnasium`
- `stable-baselines3`
- `torch`

Instalação básica:

```bash
pip install pyyaml pandas matplotlib numpy rich tqdm gymnasium "stable-baselines3[extra]"
```

Caso haja uso de GPU, a instalação do `torch` pode variar conforme CUDA. Para PPO com política MLP, o treinamento em CPU costuma ser suficiente e frequentemente mais estável em custo-benefício.

## 6. Verificação rápida do ambiente

```bash
python - <<'PY'
import gymnasium
import torch
import stable_baselines3
print('gymnasium ok')
print('torch ok:', torch.__version__, 'cuda:', torch.cuda.is_available())
print('sb3 ok:', stable_baselines3.__version__)
PY
```

## 7. Arquivos de configuração principais

### 7.1 Cenários-base

- `configs/baseline.yaml`
- `configs/baseline_queue_cap.yaml`
- `configs/baseline_timeout.yaml`
- `configs/baseline_both.yaml`

### 7.2 Sensibilidade

Em `configs/sensitivity/`, com destaque para:

- `both_ch32.yaml`
- `both_ch64.yaml`
- `both_int3.yaml`
- `both_int6.yaml`
- `both_q5_t10.yaml`
- `both_q5_t40.yaml`
- `both_q10_t20.yaml`
- `both_q15_t20.yaml`

### 7.3 RL

Em `configs/rl/`, por exemplo:

- `ppo_both.yaml`
- `ppo_both_v2.yaml`
- `ppo_both_v3.yaml`
- `ppo_both_v4.yaml`
- `robustness_v4.yaml`

## 8. Significado dos principais parâmetros YAML

### Bloco `simulation`
- `seed`: semente da execução;
- `duration_s`: duração total;
- `dt_s`: passo de tempo.

### Bloco `satellite`
- `n_beams`: número de beams;
- `total_channels`: total de canais disponíveis;
- `total_power_w`: potência total.

### Bloco `traffic`
- `base_arrival_rate`: taxa base de chegadas;
- `hotspot_amplitude`: intensidade adicional do hotspot;
- `hotspot_period_s`: período de oscilação do hotspot;
- `mean_service_demand_mb`: demanda média por requisição;
- `min_sinr_db`: limiar mínimo de SINR para atendimento.

### Bloco `channel`
- `base_snr_db`: condição de enlace base;
- `edge_loss_db`: perda espacial;
- `interference_penalty_db`: penalidade simplificada de interferência;
- `channel_bandwidth_hz`: largura de banda por canal.

### Bloco `allocation`
- `strategy`: heurística base;
- `max_channels_per_beam`: limite de canais por beam.

### Bloco `congestion`
- `enable_queue_cap`: ativa fila máxima;
- `max_queue_per_beam`: fila máxima por beam;
- `enable_timeout`: ativa timeout;
- `max_wait_s`: tempo máximo de espera.

### Bloco `rl`
- `queue_norm`, `goodput_norm`, `throughput_norm`: fatores de normalização do ambiente para RL.

### Bloco `train`
- `total_timesteps`: total de timesteps de treinamento;
- `learning_rate`, `n_steps`, `batch_size`, `gamma`, `gae_lambda`, `ent_coef`, `vf_coef`: hiperparâmetros do PPO.

### Bloco `expert` (quando existir)
- parâmetros do especialista usado para gerar dataset inicial.

### Bloco `bc` (quando existir)
- parâmetros da etapa de behavior cloning.

## 9. Natureza das abstrações do simulador

A frente Python não reproduz uma rede comercial completa nem uma constelação orbital detalhada. O ambiente foi construído como simulador experimental para estudar decisão de alocação. Portanto:

- o foco principal é o problema de redistribuição de canais;
- a topologia orbital completa foi abstraída para uma malha multifeixe fixa;
- a variabilidade espacial foi representada por hotspot;
- a camada física foi simplificada em torno de SNR, interferência e eficiência espectral;
- a carga foi modelada por requisições agregadas, e não por pacotes individuais.

Essa observação é importante porque a validade do sistema está em sua coerência com o problema estudado, e não em reproduzir todos os detalhes de uma rede industrial.

## 10. Heurísticas implementadas

As heurísticas disponíveis são:

- `proportional_fair`
- `round_robin`
- `longest_queue_first`
- `greedy_backlog`

## 11. Métricas geradas

As métricas principais geradas pelo sistema são:

- `avg_offered_load_mbps`
- `avg_accepted_load_mbps`
- `avg_capacity_mbps`
- `avg_goodput_mbps`
- `avg_queue`
- `final_queue`
- `final_blocked_rate`
- `final_blocked_queue_cap_rate`
- `final_blocked_timeout_rate`
- `avg_acceptance_rate`
- `avg_service_rate`
- `final_mean_served_delay_s`
- `final_p95_served_delay_s`
- `final_mean_timeout_delay_s`
- `final_fairness`
- `final_utilization`

## 12. Execução unitária de um cenário

Exemplo com `baseline_both`:

```bash
python scripts/run_baseline.py --config configs/baseline_both.yaml
```

Saídas típicas:

- `history.csv`
- `summary.json`
- gráficos das métricas

## 13. Execução dos experimentos principais

```bash
python scripts/run_experiments.py   --configs     configs/baseline.yaml     configs/baseline_queue_cap.yaml     configs/baseline_timeout.yaml     configs/baseline_both.yaml   --outdir results/experiments_main   --save-histories
```

Saídas esperadas:

- `results/experiments_main/all_runs.csv`
- `results/experiments_main/comparison_table.csv`
- diretórios `runs/` por cenário, estratégia e seed

## 14. Execução da sensibilidade

```bash
python scripts/run_experiments.py   --configs     configs/sensitivity/both_ch32.yaml     configs/sensitivity/both_ch64.yaml     configs/sensitivity/both_int3.yaml     configs/sensitivity/both_int6.yaml     configs/sensitivity/both_q5_t10.yaml     configs/sensitivity/both_q5_t40.yaml     configs/sensitivity/both_q10_t20.yaml     configs/sensitivity/both_q15_t20.yaml   --outdir results/experiments_sensitivity   --save-histories
```

## 15. O que muda entre as versões PPO

### `ppo_both.yaml` (`ppo_v1`)
- versão inicial estável;
- `total_timesteps = 30000`;
- reward v1.

### `ppo_both_v2.yaml`
- expansão do treinamento;
- `total_timesteps = 300000`;
- reward v2.

### `ppo_both_v3.yaml`
- refinamento do treinamento;
- `total_timesteps = 350000`;
- `learning_rate = 0.0002`;
- `ent_coef = 0.003`;
- reward final.

### `ppo_both_v4.yaml`
- mesma reward da `ppo_v3`;
- ajuste final de PPO com `total_timesteps = 250000`;
- adição de bloco `expert`;
- adição de bloco `bc` para behavior cloning;
- inicialização do agente a partir de conhecimento especialista.

### `robustness_v4.yaml`
- não define novo treinamento;
- carrega a `ppo_v4` treinada;
- executa avaliação cruzada nos cenários de sensibilidade.

## 16. Treinamento do PPO

Exemplo da versão desejada, ajustando o arquivo usado dentro de `scripts/train_rl.py`:

```bash
python scripts/train_rl.py
```

Antes de rodar, confirme qual YAML está sendo apontado no script, por exemplo:

- `configs/rl/ppo_both.yaml`
- `configs/rl/ppo_both_v2.yaml`
- `configs/rl/ppo_both_v3.yaml`
- `configs/rl/ppo_both_v4.yaml`

Saídas típicas:

- `results/rl/checkpoints/...`
- `results/rl/tensorboard/...`

## 17. Avaliação do PPO treinado

```bash
python scripts/evaluate_rl.py
```

Novamente, confirme qual YAML o script está lendo. Saídas típicas:

- `results/rl/evaluations/<versao>/rl_eval_runs.csv`
- `results/rl/evaluations/<versao>/rl_eval_summary.csv`
- subpastas por seed com `history.csv`, `summary.json` e gráficos

## 18. Comparação do PPO com heurísticas

```bash
python scripts/compare_rl_vs_heuristics.py
```

Saída típica:

- `results/rl/comparisons/<versao>/baseline_both_rl_vs_heuristics.csv`

## 19. Robustez da PPO v4

O fluxo esperado é:

1. carregar o modelo PPO v4;
2. avaliar esse mesmo modelo nos cenários de robustez;
3. consolidar os CSVs de robustez;
4. comparar PPO e heurísticas nesses mesmos cenários.

Se o projeto já tiver scripts dedicados, execute-os conforme a convenção do repositório. Caso contrário, a robustez pode ser obtida adaptando a lógica de `evaluate_rl.py` para iterar sobre os cenários listados em `robustness_v4.yaml`.

## 20. Ordem recomendada de reprodução

1. ativar a `venv`;
2. validar as bibliotecas;
3. executar um cenário unitário para smoke test;
4. rodar experimentos principais;
5. rodar sensibilidade;
6. consolidar tabelas das heurísticas;
7. treinar a versão desejada do PPO;
8. avaliar o PPO;
9. comparar PPO com heurísticas;
10. executar robustez da PPO v4;
11. consolidar figuras e tabelas finais.

## 21. Arquivos principais a usar na escrita

Para a parte textual e analítica, os arquivos mais importantes são:

- `results/experiments_main/comparison_table.csv`
- `results/experiments_sensitivity/comparison_table.csv`
- `results/rl/evaluations/<versao>/rl_eval_summary.csv`
- `results/rl/comparisons/<versao>/baseline_both_rl_vs_heuristics.csv`
- `results/rl/evaluations/robustness/ppo_both_v4/rl_robustness_summary.csv`

## 22. Observação metodológica importante sobre reward

A reward do PPO mudou entre as primeiras versões. Portanto:

- compare **todas as versões** principalmente pelas métricas operacionais do ambiente;
- use a reward como comparação direta apenas quando a formulação for a mesma, em especial entre `ppo_v3` e `ppo_v4`.

Esse cuidado evita interpretações incorretas sobre ganho artificial causado apenas por mudança de escala da função de recompensa.
