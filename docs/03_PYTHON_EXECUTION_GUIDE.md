# Guia de Execução — Frente Python do TCC LEO

## 1. Objetivo deste guia

Este documento explica, passo a passo, como instalar, configurar e executar a frente Python do TCC. O objetivo é deixar a execução reproduzível, desde os cenários base com heurísticas até os experimentos com PPO e os testes de robustez.

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

- `allocation/`: heurísticas de alocação;
- `channel/`: modelo simplificado de enlace;
- `core/`: entidades e topologia;
- `metrics/`: coleta de métricas;
- `traffic/`: geração de tráfego;
- `scenarios/`: cenário base e loop de simulação;
- `rl/`: ambiente Gymnasium, reward e alocação por prioridade para PPO.

### 3.2 `configs/`
Contém os YAMLs com os parâmetros dos experimentos.

### 3.3 `scripts/`
Contém os pontos de entrada para executar campanhas, treinar RL, avaliar modelos e comparar resultados.

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
- ambiente virtual (`venv`);
- execução principal em CPU para PPO com política MLP.

## 5. Criação do ambiente virtual

No diretório do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Atualize ferramentas básicas:

```bash
python -m pip install --upgrade pip setuptools wheel
```

## 6. Instalação das dependências

### 6.1 Dependências gerais do simulador

```bash
pip install pyyaml pandas matplotlib numpy rich tqdm
```

### 6.2 Dependências de RL

```bash
pip install gymnasium
pip install "stable-baselines3[extra]"
```

### 6.3 PyTorch

Caso deseje usar GPU CUDA, instale a versão compatível com sua máquina. No ambiente de referência foi usada uma build CUDA 12.6.

Exemplo:

```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

Verificação:

```bash
python - <<'PY'
import gymnasium
import torch
import stable_baselines3
print("gymnasium ok")
print("torch ok:", torch.__version__, "cuda:", torch.cuda.is_available())
print("sb3 ok:", stable_baselines3.__version__)
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

- `ppo_both_v1.yaml`
- `ppo_both_v2.yaml`
- `ppo_both_v3.yaml`
- `ppo_both_v4.yaml`

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



## 8.1 Natureza das abstrações do simulador

Antes da execução, é importante registrar que a frente Python não reproduz uma rede comercial completa nem uma constelação orbital detalhada. O ambiente foi construído como simulador experimental para estudar decisão de alocação. Portanto:

- o foco principal é o problema de redistribuição de canais;
- a topologia orbital completa foi abstraída para uma malha multifeixe fixa;
- a variabilidade espacial foi representada por hotspot;
- a camada física foi simplificada em torno de SNR, interferência e eficiência espectral;
- a carga foi modelada por requisições agregadas, e não por pacotes individuais.

Essa observação é importante porque a validade do sistema está em sua coerência com o problema estudado, e não em reproduzir todos os detalhes de uma rede industrial.


## 9. Heurísticas implementadas

As heurísticas disponíveis na frente Python são:

- `proportional_fair`
- `round_robin`
- `longest_queue_first`
- `greedy_backlog`

## 10. Métricas geradas

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

## 11. Execução unitária de um cenário

```bash
python scripts/run_baseline.py --config configs/baseline_both.yaml
```

## 12. Execução dos experimentos principais

```bash
python scripts/run_experiments.py   --configs     configs/baseline.yaml     configs/baseline_queue_cap.yaml     configs/baseline_timeout.yaml     configs/baseline_both.yaml   --outdir results/experiments_main   --save-histories
```

## 13. Execução da sensibilidade

```bash
python scripts/run_experiments.py   --configs     configs/sensitivity/both_ch32.yaml     configs/sensitivity/both_ch64.yaml     configs/sensitivity/both_int3.yaml     configs/sensitivity/both_int6.yaml     configs/sensitivity/both_q5_t10.yaml     configs/sensitivity/both_q5_t40.yaml     configs/sensitivity/both_q10_t20.yaml     configs/sensitivity/both_q15_t20.yaml   --outdir results/experiments_sensitivity   --save-histories
```

## 14. Verificação do ambiente RL

```bash
python scripts/smoke_test_rl.py
```

## 15. Treinamento do PPO

```bash
python scripts/train_rl.py
```

## 16. Avaliação do PPO treinado

```bash
python scripts/evaluate_rl.py
```

## 17. Comparação do PPO com heurísticas

```bash
python scripts/compare_rl_vs_heuristics.py
```

## 18. Robustez da PPO v4

A lógica geral é:

1. carregar o modelo PPO v4;
2. executar o agente nos cenários de sensibilidade;
3. salvar CSV consolidado de robustez;
4. comparar PPO e heurísticas nesses mesmos cenários.

## 19. Geração das figuras e tabelas consolidadas

```bash
python generate_tcc_summary_figures.py --base-dir . --out-dir results/tcc_compilation
```

## 20. Ordem recomendada de reprodução

1. criar e ativar a `venv`;
2. instalar dependências;
3. rodar um cenário unitário com `run_baseline.py`;
4. rodar os experimentos principais;
5. rodar os experimentos de sensibilidade;
6. validar o ambiente RL com `smoke_test_rl.py`;
7. treinar a versão desejada do PPO;
8. avaliar o PPO;
9. comparar PPO com heurísticas;
10. executar robustez do PPO v4;
11. gerar figuras e tabelas consolidadas.

## 21. Observação metodológica final

A leitura correta da frente Python não é apenas “qual método teve mais goodput”. O sistema foi construído para observar compromisso entre throughput, bloqueio, atraso, fairness e acúmulo de fila. Por isso, os experimentos devem sempre ser interpretados em conjunto com as tabelas consolidadas.
