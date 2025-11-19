import matplotlib.pyplot as plt
import numpy as np
import os

class GraphGenerator:
    def __init__(self, output_dir='graficos'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = {
            'schedule_0': '#FF6B6B',
            'schedule_9': '#4ECDC4',
            'schedule_5': '#45B7D1',
            'schedule_6': '#FF8C42',  
            'schedule_8': '#9B59B6', 
            'initial': '#45b7d1', 
            'final': '#ff6b6b',  
            'best': '#AA96DA',
            'current': '#D946A6'
        }
    
    def plot_route(self, cities, route, title, filename, color):
        fig, ax = plt.subplots(figsize=(10, 10))

        x = [cities[i][0] for i in route] + [cities[route[0]][0]]
        y = [cities[i][1] for i in route] + [cities[route[0]][1]]

        ax.plot(x, y, '-', color=color, linewidth=2.5, alpha=0.7, zorder=1)

        ax.plot(x[:-1], y[:-1], 'o', color=color, markersize=12, alpha=0.9, zorder=2)

        ax.plot(cities[route[0]][0], cities[route[0]][1], 'o', 
                color=color, markersize=20, label='Cidade Inicial', zorder=4,
                markeredgecolor='white', markeredgewidth=2.5)

        for i, city_idx in enumerate(route):
            ax.annotate(str(i), (cities[city_idx][0], cities[city_idx][1]),
                       fontsize=8, ha='center', va='center', fontweight='bold',
                       color='white', zorder=5,
                       bbox=dict(boxstyle='circle,pad=0.3', facecolor=color, 
                                alpha=0.85, edgecolor='white', linewidth=1.5))
        
        ax.set_xlabel('Coordenada X', fontsize=12, fontweight='bold')
        ax.set_ylabel('Coordenada Y', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=10, loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_cost_evolution(self, history, title, filename, color, temperatures=None):
        """Plota a evolução do custo ao longo das iterações com temperatura sobreposta."""
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        iterations = history['iterations']
        current_costs = history['current_costs']
        best_costs = history['best_costs']
        reheat_points = history.get('reheat_points', [])
        
        ax1.plot(iterations, current_costs, color=color, 
                linewidth=1.5, alpha=0.4, label='Custo Atual')
        ax1.plot(iterations, best_costs, color=color, 
                linewidth=2.5, label='Melhor Custo')

        min_cost = min(best_costs)
        min_idx = best_costs.index(min_cost)
        min_iteration = iterations[min_idx]
        ax1.plot(min_iteration, min_cost, 'o', color=color, markersize=14, 
                markeredgecolor='white', markeredgewidth=2.5, 
                label=f'Mínimo: {min_cost:.2f}', zorder=10)

        if reheat_points:
            for point in reheat_points:
                ax1.axvline(x=point, color='red', linestyle='--', alpha=0.5, linewidth=1)
            ax1.axvline(x=reheat_points[0], color='red', linestyle='--', 
                       alpha=0.5, linewidth=1, label='Reaquecimento')
        
        ax1.set_xlabel('Iteração', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Custo', fontsize=12, fontweight='bold')
        ax1.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True, alpha=0.3)

        if temperatures is not None:
            ax2 = ax1.twinx()
            ax2.plot(iterations, temperatures, color='gray', 
                    linewidth=2, linestyle='--', alpha=0.6, label='Temperatura')
            ax2.set_ylabel('Temperatura', fontsize=12, fontweight='bold')
            ax2.legend(loc='upper right', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_temperature_evolution(self, history, title, filename):
        """Plota a evolução da temperatura ao longo das iterações com marcadores de reaquecimento."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        iterations = history['iterations']
        temperatures = history['temperatures']
        reheat_points = history.get('reheat_points', [])
        
        ax.plot(iterations, temperatures, color=self.colors['schedule_5'], 
                linewidth=2.5)

        if reheat_points:
            for point in reheat_points:
                ax.axvline(x=point, color='red', linestyle='--', alpha=0.5, linewidth=2)
            ax.axvline(x=reheat_points[0], color='red', linestyle='--', 
                      alpha=0.5, linewidth=2, label='Reaquecimento')
        
        ax.set_xlabel('Iteração', fontsize=12, fontweight='bold')
        ax.set_ylabel('Temperatura', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        if reheat_points:
            ax.legend(fontsize=10, loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_complete_analysis(self, history, title, filename):
        """Plota análise completa com custo, melhor custo e temperatura."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        iterations = history['iterations']
        current_costs = history['current_costs']
        best_costs = history['best_costs']
        temperatures = history['temperatures']
        reheat_points = history.get('reheat_points', [])

        ax1.plot(iterations, current_costs, color=self.colors['current'], 
                linewidth=1.5, alpha=0.6, label='Custo Atual')
        ax1.plot(iterations, best_costs, color=self.colors['best'], 
                linewidth=2.5, label='Melhor Custo')

        min_cost = min(best_costs)
        min_idx = best_costs.index(min_cost)
        min_iteration = iterations[min_idx]
        ax1.plot(min_iteration, min_cost, 'o', color=self.colors['best'], markersize=14, 
                markeredgecolor='white', markeredgewidth=2.5, 
                label=f'Mínimo: {min_cost:.2f}', zorder=10)

        if reheat_points:
            for point in reheat_points:
                ax1.axvline(x=point, color='red', linestyle='--', alpha=0.3, linewidth=1)
        
        ax1.set_xlabel('Iteração', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Custo', fontsize=12, fontweight='bold')
        ax1.set_title('Evolução do Custo', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        ax2.plot(iterations, temperatures, color=self.colors['schedule_5'], 
                linewidth=2.5, label='Temperatura')

        if reheat_points:
            for point in reheat_points:
                ax2.axvline(x=point, color='red', linestyle='--', alpha=0.5, linewidth=1)
            ax2.axvline(x=reheat_points[0], color='red', linestyle='--', 
                       alpha=0.5, linewidth=1, label='Reaquecimento')
        
        ax2.set_xlabel('Iteração', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Temperatura', fontsize=12, fontweight='bold')
        ax2.set_title('Evolução da Temperatura', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_comparison_routes(self, cities, initial_route, final_route, 
                               initial_cost, final_cost, filename):
        """Plota lado a lado a rota inicial e a rota final."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Rota inicial
        x_init = [cities[i][0] for i in initial_route] + [cities[initial_route[0]][0]]
        y_init = [cities[i][1] for i in initial_route] + [cities[initial_route[0]][1]]
        
        ax1.plot(x_init, y_init, '-', color=self.colors['initial'], 
                linewidth=2.5, alpha=0.7, zorder=1)
        ax1.plot(x_init[:-1], y_init[:-1], 'o', color=self.colors['initial'], 
                markersize=10, alpha=0.9, zorder=2)
        ax1.plot(cities[initial_route[0]][0], cities[initial_route[0]][1], 'o', 
                color=self.colors['initial'], markersize=18, label='Início', 
                zorder=4, markeredgecolor='white', markeredgewidth=2.5)
        
        ax1.set_xlabel('Coordenada X', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Coordenada Y', fontsize=12, fontweight='bold')
        ax1.set_title(f'Rota Inicial\nCusto: {initial_cost:.2f}', 
                     fontsize=13, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Rota final
        x_final = [cities[i][0] for i in final_route] + [cities[final_route[0]][0]]
        y_final = [cities[i][1] for i in final_route] + [cities[final_route[0]][1]]
        
        ax2.plot(x_final, y_final, '-', color=self.colors['final'], 
                linewidth=2.5, alpha=0.7, zorder=1)
        ax2.plot(x_final[:-1], y_final[:-1], 'o', color=self.colors['final'], 
                markersize=10, alpha=0.9, zorder=2)
        ax2.plot(cities[final_route[0]][0], cities[final_route[0]][1], 'o', 
                color=self.colors['final'], markersize=18, label='Início', 
                zorder=4, markeredgecolor='white', markeredgewidth=2.5)
        
        ax2.set_xlabel('Coordenada X', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Coordenada Y', fontsize=12, fontweight='bold')
        ax2.set_title(f'Rota Final Otimizada\nCusto: {final_cost:.2f}', 
                     fontsize=13, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        improvement = ((initial_cost - final_cost) / initial_cost) * 100
        plt.suptitle(f'Comparação de Rotas - Melhoria: {improvement:.2f}%', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_multiple_schedules_cost(self, results, filename):
        """Plota a convergência de múltiplos cooling schedules no mesmo gráfico."""
        fig, ax = plt.subplots(figsize=(14, 7))
        
        schedule_names = {
            'schedule_0': 'Cooling Schedule 0',
            'schedule_5': 'Cooling Schedule 5',
            'schedule_6': 'Cooling Schedule 6',
            'schedule_8': 'Cooling Schedule 8',
            'schedule_9': 'Cooling Schedule 9'
        }
        
        for schedule_name, result in results.items():
            iterations = result['history']['iterations']
            best_costs = result['history']['best_costs']

            if len(iterations) > 0 and len(best_costs) > 0:
                ax.plot(iterations, best_costs, linewidth=2.5, 
                       label=schedule_names.get(schedule_name, schedule_name), 
                       color=self.colors.get(schedule_name, '#000000'))
        
        ax.set_xlabel('Iteração', fontsize=12, fontweight='bold')
        ax.set_ylabel('Melhor Custo', fontsize=12, fontweight='bold')
        ax.set_title('Comparação de Convergência - Diferentes Cooling Schedules', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_multiple_schedules_temperature(self, results, filename):
        """Plota a evolução da temperatura de múltiplos cooling schedules."""
        fig, ax = plt.subplots(figsize=(14, 7))
        
        schedule_names = {
            'schedule_0': 'Cooling Schedule 0',
            'schedule_5': 'Cooling Schedule 5',
            'schedule_6': 'Cooling Schedule 6',
            'schedule_8': 'Cooling Schedule 8',
            'schedule_9': 'Cooling Schedule 9'
        }
        
        for schedule_name, result in results.items():
            iterations = result['history']['iterations']
            temperatures = result['history']['temperatures']

            if len(iterations) > 0 and len(temperatures) > 0:
                ax.plot(iterations, temperatures, linewidth=2.5, 
                       label=schedule_names.get(schedule_name, schedule_name), 
                       color=self.colors.get(schedule_name, '#000000'))
        
        ax.set_xlabel('Iteração', fontsize=12, fontweight='bold')
        ax.set_ylabel('Temperatura', fontsize=12, fontweight='bold')
        ax.set_title('Comparação de Evolução da Temperatura - Diferentes Cooling Schedules', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_all_costs_overlapped(self, results, filename):
        """Plota todos os custos (atual e melhor) sobrepostos para todos os schedules."""
        fig, ax = plt.subplots(figsize=(14, 7))
        
        schedule_names = {
            'schedule_0': 'Cooling Schedule 0',
            'schedule_5': 'Cooling Schedule 5',
            'schedule_6': 'Cooling Schedule 6',
            'schedule_8': 'Cooling Schedule 8',
            'schedule_9': 'Cooling Schedule 9'
        }
        
        for schedule_name, result in results.items():
            iterations = result['history']['iterations']
            current_costs = result['history']['current_costs']
            best_costs = result['history']['best_costs']
            color = self.colors.get(schedule_name, '#000000')

            if len(iterations) > 0 and len(current_costs) > 0 and len(best_costs) > 0:
                ax.plot(iterations, current_costs, linewidth=1.5, alpha=0.3, 
                       color=color)

                ax.plot(iterations, best_costs, linewidth=2.5, 
                       label=schedule_names.get(schedule_name, schedule_name), 
                       color=color)
        
        ax.set_xlabel('Iteração', fontsize=12, fontweight='bold')
        ax.set_ylabel('Custo', fontsize=12, fontweight='bold')
        ax.set_title('Comparação de Custos - Todos os Cooling Schedules', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_boxplot_comparison(self, multiple_runs_data, filename):
        """
        Plota boxplot minimalista comparando os resultados de múltiplas execuções
        para diferentes cooling schedules com paleta de cores bonita.
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        schedule_names = {
            'schedule_0': 'Schedule 0\n(Linear)',
            'schedule_5': 'Schedule 5\n(Cosseno)',
            'schedule_6': 'Schedule 6\n(Tanh)',
            'schedule_8': 'Schedule 8\n(Exponencial)',
            'schedule_9': 'Schedule 9\n(Exp. Quadrático)'
        }

        data_to_plot = []
        labels = []
        colors_list = []
        
        for schedule_name in ['schedule_0', 'schedule_5', 'schedule_6', 'schedule_8', 'schedule_9']:
            if schedule_name in multiple_runs_data:
                data_to_plot.append(multiple_runs_data[schedule_name])
                labels.append(schedule_names[schedule_name])
                colors_list.append(self.colors[schedule_name])

        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                        notch=False, showmeans=True,
                        meanprops=dict(marker='D', markerfacecolor='white', 
                                     markeredgecolor='black', markersize=8, linewidth=1.5),
                        medianprops=dict(color='white', linewidth=2.5),
                        boxprops=dict(linewidth=0, edgecolor='none'), 
                        whiskerprops=dict(linewidth=2, color='#95a5a6'),
                        capprops=dict(linewidth=2, color='#95a5a6'),
                        flierprops=dict(marker='o', markerfacecolor='#E74C3C', 
                                      markersize=7, linestyle='none',
                                      markeredgecolor='none', alpha=0.6))

        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.85)
            patch.set_edgecolor('none') 
        
        ax.axhline(y=426, color='#27AE60', linestyle='--', linewidth=2.5, 
                  label='Ótimo Conhecido (426)', alpha=0.7, zorder=0)
        
        ax.set_ylabel('Custo Final', fontsize=13, fontweight='bold')
        ax.set_xlabel('Cooling Schedule', fontsize=13, fontweight='bold')
        ax.set_title('Comparação de Desempenho: 10 Execuções por Schedule', 
                    fontsize=15, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.2, axis='y', linestyle='--', linewidth=0.8)
        ax.legend(fontsize=12, loc='upper right', framealpha=0.95)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        note = ('◆ = Média | ━ = Mediana | Box = Q1-Q3\nWhiskers = Min-Max | ○ = Outliers')
        ax.text(0.02, 0.98, note, transform=ax.transAxes, 
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                        alpha=0.9, edgecolor='#bdc3c7', linewidth=1))
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Boxplot salvo: {filename}")
    
    def generate_all_graphs(self, result, schedule_name):
        """Gera todos os gráficos para um resultado específico."""
        cities = result['cities']
        initial_route = result['initial_route']
        best_route = result['best_route']
        initial_cost = result['initial_cost']
        best_cost = result['best_cost']
        history = result['history']
        
        display_name = schedule_name.replace('_', ' ').title()

        self.plot_route(cities, initial_route, 
                       f'Rota Inicial - {display_name}',
                       f'rota_inicial_{schedule_name}.png',
                       self.colors['initial'])
        
        self.plot_route(cities, best_route, 
                       f'Rota Final - {display_name}',
                       f'rota_final_{schedule_name}.png',
                       self.colors['final'])
        
        self.plot_comparison_routes(cities, initial_route, best_route, 
                                   initial_cost, best_cost,
                                   f'comparacao_rotas_{schedule_name}.png')
        
        self.plot_cost_evolution(history, 
                                f'Evolução do Custo - {display_name}',
                                f'evolucao_custo_{schedule_name}.png',
                                self.colors[schedule_name],
                                temperatures=history['temperatures'])
        
        self.plot_temperature_evolution(history, 
                                       f'Evolução da Temperatura - {display_name}',
                                       f'evolucao_temperatura_{schedule_name}.png')
        
        self.plot_complete_analysis(history, 
                                   f'Análise Completa - {display_name}',
                                   f'analise_completa_{schedule_name}.png')