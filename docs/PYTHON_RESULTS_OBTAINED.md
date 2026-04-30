# Frente Python — Resultados Obtidos

## 1. Objetivo desta seção

Esta seção consolida os principais resultados obtidos com a frente experimental em Python. O foco está em:

- comparação entre heurísticas;
- análise de sensibilidade;
- evolução do agente PPO;
- comparação final entre PPO v4 e heurísticas;
- teste de robustez da PPO v4.

## 2. Cenário principal: baseline_both

O cenário principal adotado foi o `baseline_both`, por combinar simultaneamente:
- limitação de fila por beam;
- descarte por timeout;
- carga variável com hotspot;
- competição por canais entre múltiplos beams.

Esse cenário foi tratado como referência central porque representa a condição mais completa entre os testes da frente Python.

## 3. Comparação das heurísticas no cenário principal

### 3.1 Resultado geral

No cenário `baseline_both`, a heurística `greedy_backlog` apresentou o maior goodput médio, cerca de **192.09 Mbps**, além da menor taxa final de bloqueio, aproximadamente **0.725**.

As heurísticas intermediárias ficaram em uma faixa menor:
- `proportional_fair`: **157.63 Mbps**
- `longest_queue_first`: **153.06 Mbps**
- `round_robin`: **152.48 Mbps**

### 3.2 Interpretação

A `greedy_backlog` concentrou recursos de forma mais agressiva nos beams mais carregados. Isso elevou a vazão útil e a taxa de serviço, mas também produziu maior atraso médio servido final, cerca de **15.56 s**.

Já as heurísticas intermediárias ficaram mais equilibradas, mas com menor capacidade de drenagem do backlog sob hotspot. Entre elas:
- `proportional_fair` foi a melhor em goodput;
- `round_robin` teve o menor atraso médio servido final entre as heurísticas;
- `longest_queue_first` ficou próxima de `round_robin`, mas sem vantagem consistente no cenário principal.

### 3.3 Leitura metodológica

Esse bloco foi importante para definir:
- um teto heurístico agressivo (`greedy_backlog`);
- uma faixa intermediária de desempenho (`proportional_fair`, `round_robin`, `longest_queue_first`).

Foi contra essa base que o aprendizado por reforço passou a ser comparado.

## 4. Análise de sensibilidade

### 4.1 Objetivo

A análise de sensibilidade foi conduzida com `proportional_fair` como política de referência, para verificar se o simulador respondia de forma coerente a alterações estruturais do ambiente.

### 4.2 Variação no número de canais

- `both_ch32`: goodput médio de **106.56 Mbps**
- `both_ch64`: goodput médio de **205.13 Mbps**

Interpretação:
- menos canais comprimem a capacidade de atendimento;
- mais canais ampliam a capacidade útil e reduzem o bloqueio.

### 4.3 Variação na interferência

- `both_int3`: goodput médio de **177.47 Mbps**
- `both_int6`: goodput médio de **138.45 Mbps**

Interpretação:
- interferência menor preserva eficiência espectral;
- interferência maior degrada SINR efetiva e reduz vazão realizável.

### 4.4 Variação em fila e timeout

- `both_q5_t10`: goodput de **162.30 Mbps**, atraso servido final de **7.33 s**
- `both_q5_t40`: goodput de **152.22 Mbps**, atraso servido final de **30.11 s**

Interpretação:
- timeout curto remove requisições antigas mais cedo, reduz atraso e fila;
- timeout longo preserva mais requisições em espera, mas piora atraso e tende a reduzir eficiência operacional.

### 4.5 Relaxamento da fila

- `both_q10_t20`: goodput de **159.25 Mbps**
- `both_q15_t20`: goodput de **159.31 Mbps**

Interpretação:
após certo ponto, aumentar a fila não gera ganho relevante, porque o timeout passa a dominar a contenção do sistema.

### 4.6 Conclusão da sensibilidade

A sensibilidade confirmou que o ambiente Python responde de forma coerente a alterações de:
- capacidade;
- interferência;
- fila máxima;
- timeout.

Isso fortalece a validade do simulador como ambiente experimental.

## 5. Evolução do agente PPO

### 5.1 Motivação

Após consolidar as heurísticas, foi iniciada a construção de um agente baseado em aprendizado por reforço, com PPO.

O objetivo não era apenas reproduzir uma heurística fixa, mas aprender uma política adaptativa a partir da interação com o ambiente.

### 5.2 Evolução entre versões

As versões avaliadas foram:
- PPO v1
- PPO v2
- PPO v3
- PPO v4

Goodput médio observado:
- `ppo_v1`: **153.17 Mbps**
- `ppo_v2`: **155.80 Mbps**
- `ppo_v3`: **156.23 Mbps**
- `ppo_v4`: **159.50 Mbps**

### 5.3 Interpretação

Houve evolução progressiva entre versões, com ganho de goodput e estabilização do comportamento do agente. A PPO v4 foi a versão mais forte, consolidando o melhor resultado final entre os agentes treinados.

A leitura correta não é centrada apenas na recompensa, mas principalmente nas métricas de rede:
- goodput;
- bloqueio;
- aceitação;
- serviço;
- atraso;
- fila.

## 6. Comparação final entre PPO v4 e heurísticas

### 6.1 Resultado geral

No cenário `baseline_both`, a PPO v4 atingiu:
- goodput médio de **159.50 Mbps**
- bloqueio final de **0.772**
- aceitação média de **0.823**
- serviço médio de **0.211**
- atraso servido final de **14.04 s**

### 6.2 Comparação com heurísticas

A PPO v4:
- superou `round_robin`;
- superou `longest_queue_first`;
- ficou muito próxima de `proportional_fair`;
- permaneceu abaixo de `greedy_backlog` em vazão absoluta.

### 6.3 Principal destaque

O principal ponto positivo da PPO v4 foi ter alcançado:
- desempenho competitivo em goodput;
- e o **menor atraso médio servido final** entre todas as estratégias comparadas.

Isso mostra que o agente aprendeu uma política de compromisso entre vazão, atraso e contenção de congestionamento, e não apenas uma imitação direta da heurística mais agressiva.

## 7. Robustez da PPO v4

### 7.1 Objetivo

Depois de consolidada como versão final, a PPO v4 foi avaliada em múltiplos cenários de robustez, usando alterações equivalentes às da análise de sensibilidade.

### 7.2 Resultados principais

- `both_ch32`: **107.45 Mbps**
- `both_ch64`: **210.94 Mbps**
- `both_int3`: **179.87 Mbps**
- `both_int6`: **139.65 Mbps**
- `both_q5_t10`: **165.54 Mbps**
- `both_q5_t40`: **153.65 Mbps**
- `both_q10_t20`: **159.10 Mbps**
- `both_q15_t20`: **159.10 Mbps**

### 7.3 Interpretação

A PPO v4 preservou a mesma direção de resposta observada nas heurísticas:

- com mais canais, o desempenho sobe;
- com menos canais, o desempenho cai;
- com menor interferência, o goodput cresce;
- com maior interferência, o goodput diminui;
- com timeout menor, o atraso cai;
- com timeout maior, o atraso cresce fortemente.

Isso indica que a política aprendida não ficou presa ao cenário de treinamento, tendo capturado regularidades estruturais do problema.

## 8. Síntese final da frente Python

A frente Python permitiu estabelecer quatro conclusões centrais:

1. As heurísticas definiram claramente a faixa de desempenho do problema.  
2. A análise de sensibilidade validou a coerência do simulador.  
3. O agente PPO evoluiu progressivamente até uma versão final competitiva.  
4. A PPO v4 mostrou desempenho parelho ou superior ao grupo intermediário de heurísticas, com forte destaque em atraso médio servido final e boa robustez.

A principal contribuição da frente Python não foi superar a política agressiva `greedy_backlog` em todos os critérios, mas demonstrar que uma política aprendida por reforço pode competir de forma séria com heurísticas relevantes, preservando adaptabilidade em cenários distintos.

## 9. Recomendações de figuras

### Bloco 1 — Heurísticas no cenário principal
- imagem: **baseline_both - goodput médio**
- imagem: **baseline_both - taxa final de bloqueio**
- imagem: **baseline_both - atraso médio servido final**

### Bloco 2 — Sensibilidade
- imagem: **sensibilidade proportional_fair - goodput médio**
- imagem: **sensibilidade proportional_fair - taxa final de bloqueio**

### Bloco 3 — Evolução PPO
- imagem: **evolução PPO - goodput médio**
- imagem: **evolução PPO - recompensa por episódio**
- opcional: **boxplot de goodput por seed entre versões**
- opcional: **boxplot de reward por seed entre versões**

### Bloco 4 — Robustez PPO v4
- imagem: **robustez PPO v4 - goodput médio por cenário**
- imagem: **robustez PPO v4 - taxa final de bloqueio por cenário**
- opcional: **boxplot de goodput por seed na robustez**

## 10. Observação final

Este arquivo consolida a interpretação da frente Python sem depender ainda da integração final com a frente NS-3. Por isso, ele pode ser usado como base independente para escrita, revisão e reorganização futura do capítulo de resultados.