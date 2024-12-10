import random

items = [
    {"weight": 10, "value": 60},
    {"weight": 20, "value": 100},
    {"weight": 30, "value": 120},
    {"weight": 15, "value": 75  },
    {"weight": 25, "value": 90}
]
knapsack_limit = 50

class Chromosome:
    def __init__(self, genes=None):
        # Initialize with random genes or given genes
        self.genes = genes if genes else [random.randint(0, 1) for _ in range(len(items))]
        self.fitness = 0
        self.calculate_fitness()

    def calculate_fitness(self):
        total_value = 0
        total_weight = 0
        for i, gene in enumerate(self.genes):
            if gene == 1:
                total_weight += items[i]["weight"]
                total_value += items[i]["value"]
        # Set fitness to total value if within weight limit, else 0
        if total_weight <= knapsack_limit:
            self.fitness = total_value 
        else:
            self.fitness = 0

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, crossover_rate, generations):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.population = []
        self.initialize_population()

    def initialize_population(self):
        # Create an initial random population of chromosomes
        self.population = [Chromosome() for _ in range(self.population_size)]

    def selection(self):
        total_fitness = sum(chromosome.fitness for chromosome in self.population)
        if total_fitness == 0:
            return random.choice(self.population)
        
        pick = random.uniform(0, total_fitness)

        current = 0
        for chromosome in self.population:
            current += chromosome.fitness
            if current >= pick:
                return chromosome
            
        return self.population[-1]

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate: #prob rate if to change the parents or not
            crossover_point = random.randint(1, len(parent1.genes) - 1)
            child1_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
            child2_genes = parent2.genes[:crossover_point] + parent1.genes[crossover_point:]
            return Chromosome(child1_genes), Chromosome(child2_genes)
        return parent1, parent2 #unchanged

    def mutate(self, chromosome):
        for i in range(len(chromosome.genes)):
            if random.random() < self.mutation_rate:
                chromosome.genes[i] = 1 - chromosome.genes[i]  
        chromosome.calculate_fitness()

    def evolve(self):
        for generation in range(self.generations):
            new_population = []
            while len(new_population) < self.population_size:
                #Selection
                parent1 = self.selection()
                parent2 = self.selection()

                #Crossover
                child1, child2 = self.crossover(parent1, parent2)

                #Mutation
                self.mutate(child1)
                self.mutate(child2)

                new_population.extend([child1, child2])

            # Update population and track the best solution
            self.population = new_population[:self.population_size]
            best_solution = self.get_best_solution()
            print(f"Generation {generation + 1}: Best Fitness = {best_solution.fitness}")

    def get_best_solution(self):
        # Identify and return the best chromosome in the population
        return max(self.population, key=lambda chrom: chrom.fitness)

population_size = 10
mutation_rate = 0.01
crossover_rate = 0.7
generations = 20

ga = GeneticAlgorithm(population_size, mutation_rate, crossover_rate, generations)
ga.evolve()
best_solution = ga.get_best_solution()
print("Best solution genes:", best_solution.genes)
print("Best solution fitness:", best_solution.fitness)
