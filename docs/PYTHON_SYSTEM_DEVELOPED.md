# Frente Python — Sistema Desenvolvido

## 1. Objetivo do sistema desenvolvido

O sistema desenvolvido em Python foi criado como o ambiente principal de simulação e avaliação do TCC. Seu objetivo é estudar a alocação dinâmica de canais em uma rede LEO multifeixe simplificada, sob condições de carga variável, contenção de recursos e degradação simplificada do enlace.

O foco principal do sistema não é reproduzir toda a pilha física e orbital de uma rede NTN real, mas fornecer um ambiente controlado e interpretável para comparar políticas de alocação e analisar seus efeitos sobre métricas operacionais relevantes.

## 2. Papel metodológico do simulador

O simulador em Python foi adotado como ambiente principal porque oferece:

- rapidez de prototipação;
- facilidade de modificação;
- integração direta com bibliotecas científicas e de RL;
- repetibilidade experimental;
- comparação justa entre heurísticas e aprendizado por reforço.

Ele foi usado para definir e explorar o problema de decisão, enquanto a frente em NS-3 permanece como extensão complementar para observação mais fiel em nível de rede.

## 3. Estrutura geral do simulador

O sistema foi organizado de forma modular. Em termos conceituais, ele inclui:

- topologia dos beams;
- geração de tráfego;
- modelagem simplificada do enlace;
- módulo de alocação de canais;
- coleta de métricas;
- execução de campanhas experimentais;
- integração com aprendizado por reforço.

Essa separação foi importante para permitir a reutilização do mesmo ambiente entre diferentes estratégias de decisão.

## 4. Topologia e representação dos beams

A rede foi modelada como um conjunto de beams organizados em malha hexagonal abstrata. Essa escolha foi adotada para representar, de maneira simples e controlada, um cenário multifeixe com relações locais de adjacência.

Essa modelagem não pretende reproduzir a geometria exata de um payload satelital real. Seu papel é permitir que a competição entre beams e o efeito da interferência entre vizinhos sejam estudados sem introduzir complexidade orbital e geométrica excessiva.

## 5. Geração de tráfego

O tráfego foi modelado com base em:

- taxa base de chegada;
- hotspot móvel no tempo;
- demanda média por requisição;
- assimetria espacial e temporal de carga.

Essa escolha permite representar um comportamento coerente com redes multifeixe reais, em que a carga não é uniforme entre regiões de cobertura. O hotspot foi usado como forma sintética e controlada de induzir sobrecarga localizada.

## 6. Modelo simplificado de enlace

A qualidade do enlace foi representada a partir de três componentes principais:

- SNR base;
- perda por borda do beam;
- penalidade de interferência entre beams vizinhos.

A partir disso, foi estimada uma condição de SINR efetiva e, com base nela, uma eficiência espectral simplificada, usada para converter canais alocados em capacidade de atendimento.

Esse modelo não representa um orçamento de enlace físico completo. Ele foi construído como uma abstração fenomenológica capaz de preservar a lógica causal central do problema:
- maior interferência reduz qualidade;
- pior qualidade reduz eficiência;
- menor eficiência reduz capacidade útil.

## 7. Mecanismos de contenção e congestão

O simulador incorpora mecanismos explícitos de contenção, incluindo:

- backlog por beam;
- fila máxima por beam;
- descarte por timeout;
- bloqueio acumulado;
- bloqueio por fila máxima;
- bloqueio por timeout.

Esses mecanismos foram fundamentais para transformar a alocação em um problema mais realista de decisão sob saturação, permitindo observar não apenas throughput, mas também custo operacional em termos de atraso e descarte.

## 8. Estratégias heurísticas implementadas

Foram implementadas quatro heurísticas principais:

### 8.1 Proportional Fair
Busca equilibrar atendimento da demanda e distribuição de recursos, funcionando como política intermediária entre eficiência e justiça.

### 8.2 Round Robin
Distribui canais de forma cíclica entre beams ativos. Serve como baseline uniforme e simples.

### 8.3 Longest Queue First
Prioriza beams com maior backlog, favorecendo pontos mais congestionados.

### 8.4 Greedy Backlog
Concentra recursos de forma mais agressiva nos beams mais pressionados, funcionando como política mais orientada à maximização de vazão útil.

## 9. Integração com aprendizado por reforço

A mesma base do simulador foi integrada a um ambiente compatível com Gymnasium para viabilizar treinamento por aprendizado por reforço.

O agente observa o estado do sistema e produz um vetor de prioridades para os beams. Essas prioridades são convertidas em alocação efetiva de canais respeitando as restrições do cenário.

O algoritmo utilizado foi PPO, por meio de Stable-Baselines3.

## 10. Variáveis observadas pelo agente

O estado usado no RL foi composto por informações normalizadas sobre:

- ocupação das filas;
- alocação de canais;
- qualidade estimada do enlace;
- throughput por beam;
- indicadores globais do estado instantâneo da rede.

Isso transformou o problema em uma tarefa de decisão sequencial sobre alocação adaptativa sob congestionamento.

## 11. Métricas monitoradas

O sistema registra métricas temporais e agregadas, entre elas:

- carga oferecida;
- carga aceita;
- capacidade alocada;
- goodput real;
- fila total;
- bloqueio total;
- bloqueio por fila;
- bloqueio por timeout;
- taxa de aceitação;
- taxa de serviço;
- atraso médio das requisições servidas;
- atraso P95;
- atraso médio de timeout;
- utilização de canais;
- fairness de Jain.

A coleta desse conjunto foi importante para evitar análise baseada apenas em throughput.

## 12. Configurações experimentais principais

Os cenários foram definidos por arquivos YAML, o que permitiu repetição sistemática e testes de sensibilidade. Entre os parâmetros mais importantes estão:

- número de beams;
- canais totais;
- potência total;
- intensidade do hotspot;
- demanda média por requisição;
- interferência;
- limite de fila;
- timeout.

As variações principais usadas nos experimentos envolveram:
- total de canais: 32, 48 e 64;
- penalidade de interferência: 3.0, 4.5 e 6.0;
- fila máxima por beam: 5, 10 e 15;
- timeout: 10, 20 e 40 segundos.

## 13. Fundamentação e abstrações do simulador

O simulador foi construído a partir de uma combinação entre fundamentos reais da literatura e abstrações de engenharia.

### 13.1 Elementos ancorados na literatura
Foram tomados como base conceitual:
- redes LEO multifeixe;
- interferência co-canal entre beams;
- carga desigual no espaço e no tempo;
- limitação de recursos;
- necessidade de alocação adaptativa;
- uso de RL para decisão dinâmica em redes satelitais.

### 13.2 Abstrações deliberadamente adotadas
Foram adotadas simplificações para manter o problema tratável:
- malha hexagonal abstrata de beams;
- hotspot sintético em vez de mobilidade orbital completa;
- modelo simplificado de SNR, perda de borda e interferência;
- fila máxima e timeout como parâmetros experimentais;
- ausência de modelagem física completa de propagação e protocolo.

### 13.3 Critério de escolha dos parâmetros
Os parâmetros foram escolhidos por coerência experimental, isto é, para gerar cenários:
- contrastantes;
- repetíveis;
- interpretáveis;
- comparáveis entre si.

O objetivo não foi calibrar o simulador para um operador real específico, mas gerar um ambiente adequado à comparação entre estratégias de alocação.

## 14. Reprodutibilidade

A estrutura foi preparada para:
- múltiplas seeds;
- execução em lote;
- consolidação em CSV e JSON;
- geração automática de gráficos;
- comparação entre heurísticas e versões do PPO.

Isso permitiu transformar o simulador em uma base experimental completa, e não apenas em um código de teste isolado.

## 15. Recomendações de figuras para esta documentação

### Figura recomendada 1
**Visão geral da frente Python**  
Entraria logo após a seção “Estrutura geral do simulador”.

### Figura recomendada 2
**Fluxo operacional do simulador por passo de tempo**  
Entraria após a seção “Mecanismos de contenção e congestão”.

### Figura recomendada 3
**Integração entre ambiente Python e agente PPO**  
Entraria após a seção “Integração com aprendizado por reforço”.

## 16. Síntese

O sistema em Python foi o núcleo efetivamente desenvolvido nesta etapa do trabalho. Ele foi construído como um ambiente experimental próprio, modular, controlado e reprodutível, voltado à análise de alocação dinâmica de canais em redes LEO multifeixe simplificadas. Sua principal força está em permitir comparação sistemática entre heurísticas e políticas aprendidas, preservando interpretabilidade e controle metodológico.