# TCC NTN LEO - Base Python

Base inicial para experimentos de simulação NTN LEO focados em alocação dinâmica de canais.

## Objetivo da v0

Esta versão prioriza:
- iteração rápida em Python;
- cenário simplificado e reproduzível;
- métricas de bloqueio, throughput, utilização e justiça;
- estrutura pronta para posterior migração parcial para ns-3.

## Execução rápida

```powershell
conda env create -f environment.yml
conda activate tcc_ntn_leo
python scripts/run_baseline.py --config configs/baseline.yaml
```
