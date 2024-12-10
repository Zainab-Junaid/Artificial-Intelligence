import random
import numpy as np

# Define the distance matrix
def create_distance_matrix(num_cities):
    # Random symmetric distance matrix for simplicity
    distance_matrix = np.random.randint(10, 100, size=(num_cities, num_cities))
    np.fill_diagonal(distance_matrix, 0)  # Distance from a city to itself is zero
    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance_matrix[j][i] = distance_matrix[i][j]  # Symmetric matrix
    return distance_matrix

# Initialize population with random tours
def initialize_population(pop_size, num_cities):
    population = []
    while len(population) < pop_size:
        for _ in range(pop_size):
            tour = list(range(num_cities))  # Create a list of cities as integers, e.g., [0, 1, 2, ..., num_cities-1]
            random.shuffle(tour)
            if tour not in population:  # Check for uniqueness
                population.append(tour)
    return population

# Calculate total distance of a tour
def calculate_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i]][tour[i + 1]]
    total_distance += distance_matrix[tour[-1]][tour[0]]  # Return to start
    return total_distance

# Evaluate fitness for each tour
def evaluate_fitness(population, distance_matrix):
    fitness = []
    for tour in population:
        distance = calculate_distance(tour, distance_matrix)
        fitness.append(1 / distance)  # Inverse of distance for fitness
    return fitness

# Select parents based on fitness
def select_parents(population, fitness):
    # Using roulette wheel selection
    fitness_sum = sum(fitness)
    probabilities = [f / fitness_sum for f in fitness]
    parents = random.choices(population, weights=probabilities, k=2)
    return parents

# Crossover to create offspring
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    # Copy a slice from parent1
    child[start:end + 1] = parent1[start:end + 1]
    
    # Fill the remaining positions with genes from parent2
    p2_index = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]
    
    return child

# Mutation to introduce diversity
def mutate(tour, mutation_rate=0.01):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour

# Genetic Algorithm for TSP
def genetic_algorithm_tsp(distance_matrix, pop_size=10, num_generations=100, mutation_rate=0.1):
    num_cities = len(distance_matrix)
    population = initialize_population(pop_size, num_cities)
    
    for generation in range(num_generations):
        fitness = evaluate_fitness(population, distance_matrix)
        new_population = []
        
        for _ in range(pop_size // 2):
            # Select parents
            parent1, parent2 = select_parents(population, fitness)
            # Perform crossover
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            
            # Apply mutation
            if random.random() < mutation_rate:
                child1 = mutate(child1, mutation_rate = 0.01)
            if random.random() < mutation_rate:
                child2 = mutate(child2, mutation_rate = 0.01)
            
            # Add children to the new population
            new_population.extend([child1, child2])
        
        population = new_population  # Replace old population with new population

        # Print best fitness in the current generation
        best_fitness = max(fitness)
        print(f"Generation {generation + 1} - Best Fitness: {best_fitness:.2f}")

    # Final solution
    best_tour = population[np.argmax(fitness)]
    best_distance = calculate_distance(best_tour, distance_matrix)
    
    print("\nOptimal Tour:", best_tour)
    print("Optimal Distance:", best_distance)

# Example usage
num_cities = 5
pop_size = 10
num_generations = 100

distance_matrix = create_distance_matrix(num_cities)
genetic_algorithm_tsp(distance_matrix, pop_size, num_generations)
