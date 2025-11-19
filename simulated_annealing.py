import numpy as np
import random

class SimulatedAnnealing:
    def __init__(self, instance_file, params, seed=42):
        self.seed = seed
        self.cities = self._load_cities_from_file(instance_file)
        self.n_cities = len(self.cities)
        self.distance_matrix = self._calculate_distance_matrix()
        self.normalized_distance_matrix = self._normalize_distance_matrix()
        
        self.T_0 = params['T_0']
        self.T_min = params['T_min']
        self.max_iterations = params['max_iterations']
        self.cooling_schedule = params['cooling_schedule']
        
        # Novos parâmetros para melhorar a exploração
        self.use_2opt = params.get('use_2opt', True)
        self.reheat_temp = params.get('reheat_temp', self.T_0 * 0.3)
        self.reheat_iterations = params.get('reheat_iterations', 50000)
        self.stagnation_limit = params.get('stagnation_limit', 20000)
        
        # SAmax dinâmico - número de iterações na mesma temperatura
        self.sa_max = params.get('sa_max', 1)  # Default = 1 (comportamento original)
        
        # Novo: parâmetros para reaquecimento progressivo
        self.progressive_cooling = params.get('progressive_cooling', True)
        self.reheat_cooling_rate = params.get('reheat_cooling_rate', 0.95)  # Taxa de resfriamento após reaquecimento

        self.history = {
            'iterations': [],
            'temperatures': [],
            'current_costs': [],
            'best_costs': [],
            'routes': [],
            'reheat_points': []  # Marca quando houve reaquecimento
        }
        
    def _load_cities_from_file(self, filepath):
        """Carrega coordenadas das cidades do arquivo de instância"""
        cities = []
        reading_coords = False
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Detecta início da seção de coordenadas
                if line.startswith('NODE') or line.startswith('1 '):
                    reading_coords = True
                    if not line.startswith('NODE'):
                        # Primeira linha já é uma coordenada
                        parts = line.split()
                        x, y = float(parts[1]), float(parts[2])
                        cities.append((x, y))
                    continue
                
                # Para de ler quando encontrar EOF
                if line == 'EOF' or line == '':
                    break
                
                # Lê coordenadas
                if reading_coords:
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            x, y = float(parts[1]), float(parts[2])
                            cities.append((x, y))
                        except ValueError:
                            continue
        
        return cities
    
    def _calculate_distance_matrix(self):
        """Cria uma matriz nxn com distância entre cada par de cidades (distância euclidiana)"""
        n = self.n_cities
        matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = self.cities[i][0] - self.cities[j][0]
                    dy = self.cities[i][1] - self.cities[j][1]
                    matrix[i][j] = np.sqrt(dx**2 + dy**2)
        return matrix
    
    def _normalize_distance_matrix(self):
        """Normaliza a matriz de distâncias para o intervalo [0, 1]"""
        max_distance = np.max(self.distance_matrix)
        if max_distance > 0:
            return self.distance_matrix / max_distance
        return self.distance_matrix
    
    def _calculate_route_cost(self, route, use_normalized=False):
        """Soma as distâncias entre as cidades da rota e garante que volte ao início"""
        cost = 0
        matrix = self.normalized_distance_matrix if use_normalized else self.distance_matrix
        for i in range(len(route)):
            city_a = route[i]
            city_b = route[(i + 1) % len(route)]
            cost += matrix[city_a][city_b]
        return cost
    
    def _generate_neighbor(self, route):
        """Cria solução "parecida" trocando duas cidades aleatórias (menos a primeira)"""
        new_route = route.copy()
        i, j = random.sample(range(1, self.n_cities), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route
    
    def _generate_neighbor_2opt(self, route):
        """
        Operador 2-opt: inverte um segmento da rota.
        Melhor operador de vizinhança para TSP, ajuda a evitar mínimos locais.
        """
        new_route = route.copy()
        i, j = sorted(random.sample(range(1, self.n_cities), 2))
        new_route[i:j+1] = reversed(new_route[i:j+1])
        return new_route
    
    def _cooling_schedule_0(self, iteration, total_iterations):
        """Cooling Schedule 0 (Linear): T = T_0 - i * ((T_0 - T_N) / N)"""
        return self.T_0 - iteration * ((self.T_0 - self.T_min) / total_iterations)
    
    def _cooling_schedule_9(self, iteration, total_iterations):
        """Cooling Schedule 9 (Exponencial Quadrático): T = T_0 * e^(-((1/N^2) * ln(T_0/T_N)) * i^2)"""
        N = total_iterations
        T_0 = self.T_0
        T_N = self.T_min
        i = iteration
        
        if N == 0 or T_N <= 0 or T_0 <= 0:
            return self.T_0
        
        exponent = -((1 / (N ** 2)) * np.log(T_0 / T_N)) * (i ** 2)
        return T_0 * np.exp(exponent)
    
    def _cooling_schedule_5(self, iteration, total_iterations):
        """Cooling Schedule 5 (Cosseno): T = (1/2)(T_0 - T_N) * (1 + cos((i*pi)/N)) + T_N"""
        return 0.5 * (self.T_0 - self.T_min) * (1 + np.cos((iteration * np.pi) / total_iterations)) + self.T_min
    
    def _cooling_schedule_6(self, iteration, total_iterations):
        """Cooling Schedule 6 (Tangente Hiperbólica): T = 1/2 * (T_0 - T_N) * (1 - tanh((10*i/N) - 5)) + T_N"""
        return 0.5 * (self.T_0 - self.T_min) * (1 - np.tanh((10 * iteration / total_iterations) - 5)) + self.T_min
    
    def _cooling_schedule_8(self, iteration, total_iterations):
        """Cooling Schedule 8 (Exponencial): T = T_0 * e^(-((1/N) * ln(T_0/T_N)) * i)"""
        return self.T_0 * np.exp(-((1 / total_iterations) * np.log(self.T_0 / self.T_min)) * iteration)
    
    def _get_temperature(self, iteration, total_iterations):
        """Retorna a temperatura atual baseada no cooling schedule escolhido"""
        if self.cooling_schedule == 'schedule_0':
            return self._cooling_schedule_0(iteration, total_iterations)
        elif self.cooling_schedule == 'schedule_9':
            return self._cooling_schedule_9(iteration, total_iterations)
        elif self.cooling_schedule == 'schedule_5':
            return self._cooling_schedule_5(iteration, total_iterations)
        elif self.cooling_schedule == 'schedule_6':
            return self._cooling_schedule_6(iteration, total_iterations)
        elif self.cooling_schedule == 'schedule_8':
            return self._cooling_schedule_8(iteration, total_iterations)
        else:
            raise ValueError(f"Cooling schedule '{self.cooling_schedule}' não reconhecido")
    
    def solve(self, verbose=True):
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        current_route = list(range(self.n_cities))
        random.shuffle(current_route[1:])  
        
        initial_route = current_route.copy()
        current_cost = self._calculate_route_cost(current_route)
        
        # Armazena como melhor solução
        best_route = current_route.copy()
        best_cost = current_cost
        
        # Contador de estagnação (para reaquecimento)
        iterations_without_improvement = 0
        last_best_cost = best_cost
        
        # Variáveis para reaquecimento progressivo
        is_reheating = False
        reheat_start_iteration = 0
        base_temp_at_reheat = 0
        
        if verbose:
            schedule_name = self.cooling_schedule.replace('_', ' ').title()
            print(f"\n{'='*60}")
            print(f"Executando Simulated Annealing - {schedule_name} (Seed: {self.seed})")
            print(f"{'='*60}")
            print(f"Número de cidades: {self.n_cities}")
            print(f"Custo inicial: {current_cost:.2f}")
            print(f"SAmax: {self.sa_max}")
            print(f"\n{'Iteração':<12} | {'T':<12} | {'E':<12} | {'Melhor':<12}")
            print(f"{'-'*60}")
        
        # Loop principal
        iteration = 0
        while iteration < self.max_iterations:
            T = self._get_temperature(iteration, self.max_iterations)
            
            # Reaquecimento progressivo
            if iterations_without_improvement >= self.stagnation_limit:
                if not is_reheating:
                    # Inicia reaquecimento
                    is_reheating = True
                    reheat_start_iteration = iteration
                    base_temp_at_reheat = T
                    T = self.reheat_temp
                    iterations_without_improvement = 0
                    self.history['reheat_points'].append(iteration)
                    if verbose and iteration % 10000 == 0:
                        print(f"  >>> Reaquecimento iniciado na iteração {iteration} para T={self.reheat_temp:.2f}")
            
            # Resfriamento progressivo após reaquecimento
            if is_reheating:
                iterations_since_reheat = iteration - reheat_start_iteration
                # Resfria progressivamente usando taxa geométrica
                T = self.reheat_temp * (self.reheat_cooling_rate ** iterations_since_reheat)
                
                # Para o reaquecimento quando a temperatura cair abaixo da temperatura base
                if T <= base_temp_at_reheat:
                    is_reheating = False
                    T = self._get_temperature(iteration, self.max_iterations)
            
            if T < self.T_min:
                break
            
            # SAmax: executa múltiplas iterações na mesma temperatura
            for _ in range(self.sa_max):
                # Gera vizinho: usa 2-opt se habilitado, senão usa swap simples
                if self.use_2opt and random.random() < 0.7:
                    new_route = self._generate_neighbor_2opt(current_route)
                else:
                    new_route = self._generate_neighbor(current_route)
                
                new_cost = self._calculate_route_cost(new_route)
                
                # Compara o custo novo com o anterior
                delta = new_cost - current_cost
                
                # Critério de aceitação
                if delta < 0:
                    current_route = new_route
                    current_cost = new_cost
                    
                    if current_cost < best_cost:
                        best_route = current_route.copy()
                        best_cost = current_cost
                        iterations_without_improvement = 0
                    else:
                        iterations_without_improvement += 1
                else:
                    # Se for pior, aceita às vezes
                    acceptance_prob = np.exp(-delta / T) if T > 0 else 0
                    if random.random() < acceptance_prob:
                        current_route = new_route
                        current_cost = new_cost
                    iterations_without_improvement += 1
            
            # Armazena histórico
            self.history['iterations'].append(iteration)
            self.history['temperatures'].append(T)
            self.history['current_costs'].append(current_cost)
            self.history['best_costs'].append(best_cost)
            
            if verbose and iteration % 10000 == 0:
                print(f"{iteration:<12} | {T:<12.4f} | {current_cost:<12.2f} | {best_cost:<12.2f}")
            
            iteration += 1
        
        if verbose:
            print(f"{'-'*60}")
            print(f"Custo final: {best_cost:.2f}")
            print(f"Melhoria: {((1 - best_cost/self._calculate_route_cost(initial_route)) * 100):.2f}%")
            print(f"Número de reaquecimentos: {len(self.history['reheat_points'])}")
            print(f"{'='*60}\n")
        
        return {
            'initial_route': initial_route,
            'best_route': best_route,
            'initial_cost': self._calculate_route_cost(initial_route),
            'best_cost': best_cost,
            'history': self.history,
            'cities': self.cities,
            'seed': self.seed
        }