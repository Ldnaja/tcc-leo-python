# Tabelas em LaTeX — Frente Python

## Tabela 1 — Heurísticas no cenário `baseline_both`

```latex
\begin{table}[htbp]
\centering
\caption{Heurísticas no cenário baseline\_both.}
\label{tab:baseline_both_heuristics}
\begin{tabular}{lccccccc}
\toprule
Heurística & Goodput & Bloqueio & Aceitação & Serviço & Atraso & Fairness & Fila \\
\midrule
proportional\_fair & 157.628 & 0.772 & 0.823 & 0.21 & 15.336 & 0.819 & 61.3 \\
round\_robin & 152.475 & 0.779 & 0.817 & 0.203 & 14.323 & 0.963 & 60.1 \\
longest\_queue\_first & 153.061 & 0.778 & 0.819 & 0.204 & 14.674 & 0.937 & 60.1 \\
greedy\_backlog & 192.094 & 0.725 & 0.838 & 0.252 & 15.56 & 0.985 & 62.4 \\
\bottomrule
\end{tabular}
\end{table}
```

## Tabela 2 — Sensibilidade com `proportional_fair`

```latex
\begin{table}[htbp]
\centering
\caption{Análise de sensibilidade com proportional\_fair.}
\label{tab:sensitivity_pf}
\begin{tabular}{lccccc}
\toprule
Cenário & Goodput & Bloqueio & Aceitação & Serviço & Atraso \\
\midrule
both\_ch32 & 106.565 & 0.84 & 0.814 & 0.14 & 15.576 \\
both\_ch64 & 205.125 & 0.713 & 0.832 & 0.27 & 14.951 \\
both\_int3 & 177.466 & 0.747 & 0.827 & 0.235 & 15.233 \\
both\_int6 & 138.453 & 0.798 & 0.82 & 0.183 & 15.409 \\
both\_q5\_t10 & 162.3 & 0.781 & 0.967 & 0.211 & 7.332 \\
both\_q5\_t40 & 152.222 & 0.772 & 0.592 & 0.205 & 30.113 \\
both\_q10\_t20 & 159.252 & 0.767 & 0.994 & 0.207 & 16.157 \\
both\_q15\_t20 & 159.308 & 0.767 & 1.0 & 0.207 & 16.187 \\
\bottomrule
\end{tabular}
\end{table}
```

## Tabela 3 — Evolução das versões PPO

```latex
\begin{table}[htbp]
\centering
\caption{Resumo das versões PPO avaliadas.}
\label{tab:ppo_versions}
\begin{tabular}{lcccccc}
\toprule
Versão PPO & Recompensa & Goodput & Bloqueio & Aceitação & Serviço & Atraso \\
\midrule
ppo\_v1 & -0.504 & 153.171 & 0.779 & 0.817 & 0.202 & 14.208 \\
ppo\_v2 & 4.388 & 155.804 & 0.778 & 0.821 & 0.205 & 14.051 \\
ppo\_v3 & 74.362 & 156.229 & 0.777 & 0.821 & 0.206 & 14.127 \\
ppo\_v4 & 77.459 & 159.496 & 0.772 & 0.823 & 0.211 & 14.042 \\
\bottomrule
\end{tabular}
\end{table}
```

## Tabela 4 — PPO v4 versus heurísticas

```latex
\begin{table}[htbp]
\centering
\caption{Comparação final entre PPO v4 e heurísticas no cenário baseline\_both.}
\label{tab:ppo_v4_vs_heuristics}
\begin{tabular}{lccccccc}
\toprule
Estratégia & Goodput & Bloqueio & Aceitação & Serviço & Atraso & Fairness & Fila \\
\midrule
proportional\_fair & 157.628 & 0.772 & 0.823 & 0.21 & 15.336 & 0.819 & 61.3 \\
round\_robin & 152.475 & 0.779 & 0.817 & 0.203 & 14.323 & 0.963 & 60.1 \\
longest\_queue\_first & 153.061 & 0.778 & 0.819 & 0.204 & 14.674 & 0.937 & 60.1 \\
greedy\_backlog & 192.094 & 0.725 & 0.838 & 0.252 & 15.56 & 0.985 & 62.4 \\
ppo\_v4 & 159.496 & 0.772 & 0.823 & 0.211 & 14.042 & 0.691 & 60.4 \\
\bottomrule
\end{tabular}
\end{table}
```

## Tabela 5 — Robustez da PPO v4

```latex
\begin{table}[htbp]
\centering
\caption{Resumo da robustez da PPO v4 nos cenários de sensibilidade.}
\label{tab:ppo_v4_robustness}
\begin{tabular}{lcccccc}
\toprule
Cenário & Recompensa & Goodput & Bloqueio & Aceitação & Serviço & Atraso \\
\midrule
both\_ch32 & -100.649 & 107.447 & 0.841 & 0.812 & 0.14 & 14.409 \\
both\_ch64 & 265.502 & 210.941 & 0.704 & 0.832 & 0.278 & 13.708 \\
both\_int3 & 149.148 & 179.874 & 0.747 & 0.826 & 0.236 & 13.916 \\
both\_int6 & 7.487 & 139.648 & 0.797 & 0.819 & 0.187 & 14.248 \\
both\_q5\_t10 & 132.916 & 165.541 & 0.775 & 0.966 & 0.218 & 6.759 \\
both\_q5\_t40 & 24.707 & 153.655 & 0.773 & 0.596 & 0.204 & 27.355 \\
both\_q10\_t20 & 70.114 & 159.101 & 0.769 & 0.994 & 0.208 & 14.797 \\
both\_q15\_t20 & 69.749 & 159.097 & 0.769 & 1.0 & 0.207 & 14.815 \\
\bottomrule
\end{tabular}
\end{table}
```
