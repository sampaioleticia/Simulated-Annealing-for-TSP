# Simulated Annealing para TSP

Implementação do algoritmo Simulated Annealing para resolver o Problema do Caixeiro Viajante com diferentes estratégias de resfriamento.

## Estrutura do Projeto
```
.
├── main.py                    # Execução principal e análise estatística
├── simulated_annealing.py     # Implementação do algoritmo SA
├── graphs.py                  # Geração de gráficos
├── 51_cidades.txt            # Instância eil51 (ótimo: 426)
└── 100_cidades.txt           # Instância kroA100 (ótimo: 21282)
```

## Como Executar
```bash
python main.py
```

O programa executará 10 runs para cada cooling schedule (0, 5, 6, 8, 9) e gerará estatísticas descritivas e gráficos comparativos.

## Arquivos de Dados

- **51_cidades.txt**: Instância eil51 com 51 cidades (formato TSPLIB)
- **100_cidades.txt**: Instância kroA100 com 100 cidades (formato TSPLIB)

## Saída

Os resultados serão salvos na pasta **`graficos/`** contendo:
- Gráficos de convergência individuais por schedule
- Gráficos comparativos de custo e temperatura
- Boxplots estatísticos das 10 execuções

## Configuração para 100 Cidades

No arquivo `main.py`, ajuste:
```python
INSTANCE_FILE = 'Instancias/100_cidades.txt'
T_0 = 2000.0
MAX_ITERATIONS = 800000
reheat_cooling_rate = 0.98
```