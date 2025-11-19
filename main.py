from simulated_annealing import SimulatedAnnealing
from graphs import GraphGenerator
import numpy as np

def calculate_statistics(costs):
    """
    Calcula estatísticas descritivas para uma lista de custos.
    Usa desvio padrão AMOSTRAL (n-1) para dados experimentais.
    """
    costs_array = np.array(costs)
    return {
        'mean': np.mean(costs_array),
        'std': np.std(costs_array, ddof=1),  
        'min': np.min(costs_array),
        'max': np.max(costs_array),
        'median': np.median(costs_array)
    }

def print_statistics_table(stats_dict):
    """Imprime uma tabela formatada com as estatísticas de todos os schedules."""
    print("\n" + "="*100)
    print("ESTATÍSTICAS DESCRITIVAS - 10 EXECUÇÕES POR COOLING SCHEDULE")
    print("="*100)
    print(f"{'Schedule':<15} | {'Média':<10} | {'Desvio Pad':<12} | {'Mínimo':<10} | {'Máximo':<10} | {'Mediana':<10}")
    print("-"*100)
    
    schedule_names = {
        'schedule_0': 'Schedule 0',
        'schedule_5': 'Schedule 5',
        'schedule_6': 'Schedule 6',
        'schedule_8': 'Schedule 8',
        'schedule_9': 'Schedule 9'
    }
    
    for schedule, stats in stats_dict.items():
        name = schedule_names.get(schedule, schedule)
        print(f"{name:<15} | {stats['mean']:<10.2f} | {stats['std']:<12.2f} | "
              f"{stats['min']:<10.2f} | {stats['max']:<10.2f} | {stats['median']:<10.2f}")
    
    print("="*100)
    print("Nota: Desvio Padrão calculado usando fórmula AMOSTRAL (n-1)")
    print("="*100)

def main():
    INSTANCE_FILE = 'Instancias/51_cidades.txt'
    T_0 = 1000.0
    T_MIN = 0.0005 
    MAX_ITERATIONS = 400000
    N_RUNS = 10
    SA_MAX = 7 
    SEEDS = [42, 123, 456, 789, 1011, 1314, 1617, 1920, 2223, 2526]

    # INSTANCE_FILE = 'Instancias/100_cidades.txt'
    
    params_base = {
        'T_0': T_0,
        'T_min': T_MIN,
        'max_iterations': MAX_ITERATIONS,
        'sa_max': SA_MAX,  
        'use_2opt': True, 
        'reheat_temp': T_0 * 0.3,  # Reaquece para 30% da temperatura inicial
        'stagnation_limit': 80000,  # Reaquece após 20000 iterações sem melhoria
        'progressive_cooling': True,  # Ativa resfriamento progressivo
        'reheat_cooling_rate': 0.95  # Taxa de resfriamento após reaquecimento (95% por iteração)
    }
    
    cooling_schedules = ['schedule_0', 'schedule_5', 'schedule_6', 'schedule_8', 'schedule_9']
    
    results = {}  # Resultado de UMA execução (para gráficos individuais)
    multiple_runs_costs = {}  # Custos de TODAS as 10 execuções (para boxplot e estatísticas)
    
    print("\n" + "="*60)
    print("SIMULATED ANNEALING - PROBLEMA DO CAIXEIRO VIAJANTE")
    print("="*60)
    print(f"Arquivo de instância: {INSTANCE_FILE}")
    print(f"Temperatura inicial: {T_0}")
    print(f"Temperatura mínima: {T_MIN}")
    print(f"Máximo de iterações: {MAX_ITERATIONS}")
    print(f"SAmax (iterações por temperatura): {SA_MAX}")
    print(f"Número de execuções por schedule: {N_RUNS}")
    print("="*60)
    
    for schedule in cooling_schedules:
        print(f"\n{'='*60}")
        print(f"Executando {N_RUNS} runs para {schedule.replace('_', ' ').title()}")
        print(f"{'='*60}")
        
        schedule_costs = []  # Armazena os custos finais das 10 execuções
        
        for run_idx, seed in enumerate(SEEDS):
            params = params_base.copy()
            params['cooling_schedule'] = schedule
            
            print(f"\n--- Run {run_idx + 1}/{N_RUNS} (Seed: {seed}) ---")
            
            # Cria instância do SA com seed específica
            sa = SimulatedAnnealing(INSTANCE_FILE, params, seed=seed)
            
            # Resolve o problema (verbose=False para não poluir o terminal)
            result = sa.solve(verbose=(run_idx == 0))  # Mostra detalhes só do primeiro run
            
            # Armazena o custo final desta execução
            schedule_costs.append(result['best_cost'])
            
            print(f"  ✓ Run {run_idx + 1} concluído - Custo final: {result['best_cost']:.2f}")
            
            # Salva o resultado da primeira execução para gerar gráficos depois
            if run_idx == 0:
                results[schedule] = result
        
        # Armazena todos os custos deste schedule
        multiple_runs_costs[schedule] = schedule_costs
        
        # Calcula e mostra estatísticas para este schedule
        stats = calculate_statistics(schedule_costs)
        print(f"\n  Estatísticas do {schedule.replace('_', ' ').title()}:")
        print(f"    Média:       {stats['mean']:.2f}")
        print(f"    Desvio Pad:  {stats['std']:.2f}")
        print(f"    Mínimo:      {stats['min']:.2f}")
        print(f"    Máximo:      {stats['max']:.2f}")
        print(f"    Mediana:     {stats['median']:.2f}")
    
    # Calcula estatísticas para todos os schedules
    print("\n" + "="*60)
    print("CALCULANDO ESTATÍSTICAS DESCRITIVAS...")
    print("="*60)
    
    all_statistics = {}
    for schedule, costs in multiple_runs_costs.items():
        all_statistics[schedule] = calculate_statistics(costs)
    
    # Imprime tabela de estatísticas
    print_statistics_table(all_statistics)
    
    # Gera gráficos
    print("\n" + "="*60)
    print("GERANDO GRÁFICOS...")
    print("="*60)
    
    graph_gen = GraphGenerator()
    
    # Gráficos individuais (usando o primeiro run de cada schedule)
    print("\nGráficos individuais (primeira execução de cada schedule):")
    for schedule_name, result in results.items():
        display_name = schedule_name.replace('_', ' ').title()
        print(f"  - Gráficos para {display_name}...")
        graph_gen.generate_all_graphs(result, schedule_name)

    # Gráficos comparativos
    print("\nGráficos comparativos:")
    print("  - Comparação de convergência...")
    graph_gen.plot_multiple_schedules_cost(results, 'comparacao_convergencia.png')
    
    print("  - Comparação de temperatura...")
    graph_gen.plot_multiple_schedules_temperature(results, 'comparacao_temperatura.png')
    
    print("  - Comparação de custos...")
    graph_gen.plot_all_costs_overlapped(results, 'comparacao_custo.png')
    
    # Boxplot comparativo
    print("\n  - Boxplot comparativo (10 runs)...")
    graph_gen.plot_boxplot_comparison(multiple_runs_costs, 'boxplot_comparacao_schedules.png')
    
    # Resultados finais
    print("\n" + "="*60)
    print("RESULTADOS FINAIS - COMPARAÇÃO COM ÓTIMO CONHECIDO")
    print("="*60)
    print(f"Ótimo conhecido para 51 cidades (eil51): 426.00")
    print("="*60)
    
    schedule_names = {
        'schedule_0': 'COOLING SCHEDULE 0',
        'schedule_5': 'COOLING SCHEDULE 5',
        'schedule_6': 'COOLING SCHEDULE 6',
        'schedule_8': 'COOLING SCHEDULE 8',
        'schedule_9': 'COOLING SCHEDULE 9'
    }
    
    print(f"\n{'Schedule':<20} | {'Melhor Resultado':<18} | {'Gap do Ótimo':<15} | {'Mediana':<10}")
    print("-"*75)
    
    for schedule_name in cooling_schedules:
        stats = all_statistics[schedule_name]
        best = stats['min']
        median = stats['median']
        gap = ((best - 426) / 426) * 100
        
        name = schedule_names.get(schedule_name, schedule_name)
        print(f"{name:<20} | {best:<18.2f} | {gap:>+14.2f}% | {median:<10.2f}")
    
    print("="*75)
    
    # Identifica o melhor schedule
    best_schedule = min(all_statistics.items(), key=lambda x: x[1]['min'])
    print(f"\nMELHOR SCHEDULE: {schedule_names[best_schedule[0]]}")
    print(f"   Melhor resultado: {best_schedule[1]['min']:.2f}")
    print(f"   Desvio padrão: {best_schedule[1]['std']:.2f} (mais consistente = melhor)")
    
    print(f"\nTodos os gráficos foram salvos na pasta 'graficos/'")
    print("Execução concluída com sucesso!\n")

if __name__ == "__main__":
    main()