# Frente Python — Guia de Figuras e Arquivos

## 1. Objetivo

Este arquivo organiza os principais arquivos, tabelas e figuras da frente Python, facilitando a transição posterior para LaTeX e para a montagem do capítulo final do TCC.

## 2. Arquivos-base já consolidados

### Texto-base do sistema desenvolvido
- `Texto colado.txt`

### Texto-base dos resultados
- `Texto colado (2).txt`

### Texto-base das abstrações e fundamentação metodológica
- `Texto colado (3).txt`

## 3. Blocos analíticos principais

### Bloco A — Sistema desenvolvido
Usar:
- descrição do simulador;
- arquitetura modular;
- fluxo operacional;
- bibliotecas;
- heurísticas;
- RL;
- abstrações e bases reais.

### Bloco B — Resultados das heurísticas
Usar:
- tabela de comparação no cenário `baseline_both`;
- gráficos de goodput, bloqueio e atraso.

### Bloco C — Sensibilidade
Usar:
- tabela consolidada da sensibilidade com `proportional_fair`;
- gráficos de goodput e bloqueio.

### Bloco D — Evolução PPO
Usar:
- tabela de versões PPO;
- gráfico de goodput entre versões;
- gráfico de reward entre versões;
- boxplots opcionais.

### Bloco E — Comparação final PPO v4 vs heurísticas
Usar:
- tabela final consolidada;
- reaproveitamento das figuras principais do cenário `baseline_both`.

### Bloco F — Robustez PPO v4
Usar:
- tabela de robustez;
- gráficos de robustez;
- boxplot opcional.

## 4. Figuras recomendadas por ordem

1. visão geral da frente Python  
2. fluxo operacional do simulador  
3. integração simulador + PPO  
4. baseline_both - goodput médio  
5. baseline_both - bloqueio final  
6. baseline_both - atraso médio servido final  
7. sensibilidade - goodput médio  
8. sensibilidade - bloqueio final  
9. evolução PPO - goodput  
10. evolução PPO - reward  
11. robustez PPO v4 - goodput  
12. robustez PPO v4 - bloqueio  
13. boxplot de versões PPO (opcional)  
14. boxplot de robustez PPO v4 (opcional)

## 5. Arquivos numéricos que continuam úteis

Se depois você quiser refinar ainda mais as tabelas e cruzar valores diretamente, os arquivos mais úteis continuam sendo:

- consolidação principal das heurísticas;
- consolidação da sensibilidade;
- consolidação das versões PPO;
- consolidação final PPO v4 vs heurísticas;
- consolidação da robustez PPO v4.

## 6. O que pode ser reenviado, se quiser refino máximo

No momento, não é obrigatório reenviar nada para montar esses MDs.

Mas, se depois você quiser uma versão ainda mais precisa e 100% alinhada ao material final do TCC, os arquivos mais úteis para reenviar seriam:
- CSV consolidado do `experiments_main`;
- CSV consolidado do `experiments_sensitivity`;
- CSV final de versões PPO;
- CSV final de comparação PPO v4 vs heurísticas;
- CSV final de robustez PPO v4;
- nomes exatos dos arquivos de imagem gerados.

## 7. Uso recomendado

Esses MDs podem funcionar como:
- base de escrita;
- versão intermediária antes do LaTeX;
- documentação da frente Python;
- apoio para revisão do orientador;
- material de reorganização antes da integração com NS-3.