# Frente Python — Visão Geral

## 1. Objetivo da frente Python

A frente Python constitui o ambiente principal de modelagem, experimentação e avaliação deste trabalho. Seu objetivo é investigar o problema de alocação dinâmica de canais em redes de satélites LEO multifeixe sob carga variável, comparando políticas heurísticas e políticas baseadas em aprendizado por reforço em um ambiente controlado.

Essa frente foi desenvolvida para permitir:
- modelagem modular do sistema;
- execução repetível de cenários;
- comparação entre heurísticas e RL;
- análise por múltiplas métricas;
- testes de sensibilidade e robustez.

## 2. Papel da frente Python no TCC

A frente Python é a base experimental principal do trabalho.

Ela foi usada para:
- definir o problema de decisão;
- modelar beams, tráfego, interferência simplificada, filas e restrições;
- executar heurísticas de referência;
- integrar e avaliar agentes de aprendizado por reforço;
- produzir os resultados principais desta etapa do TCC.

A frente em NS-3 será tratada posteriormente como uma verificação complementar em nível de rede, sem substituir a modelagem e os resultados centrais obtidos no simulador Python.

## 3. Organização recomendada desta documentação

A documentação condensada da frente Python pode ser organizada em três blocos principais:

- `PYTHON_SYSTEM_DEVELOPED.md`  
  descreve como o simulador foi construído, quais módulos foram implementados, quais bibliotecas foram utilizadas, como os cenários foram configurados e quais abstrações foram adotadas.

- `PYTHON_RESULTS_OBTAINED.md`  
  apresenta os resultados obtidos com heurísticas e aprendizado por reforço, incluindo análise de sensibilidade, evolução do agente PPO, comparação final com heurísticas e teste de robustez.

- `PYTHON_FIGURES_AND_FILES_GUIDE.md`  
  lista os arquivos, tabelas e figuras mais importantes para apoiar a escrita final em LaTeX.

## 4. Observação metodológica

O simulador em Python não foi construído como réplica integral de uma ferramenta industrial ou de uma pilha NTN completa. Ele foi desenvolvido como um ambiente experimental próprio, de caráter abstrato e controlado, inspirado por problemas e fenômenos recorrentes da literatura sobre redes LEO multifeixe, como interferência, carga desigual, saturação por recursos limitados, contenção por fila e tomada de decisão adaptativa.