from pathlib import Path
from .Agent import Agent
import random
from datetime import datetime
import numpy as np
import os

class Evolution:
    def __init__(self, population_size, mutation_rate, elitism_rate, tournament_size = 0.1, seed = 42):
        self.name = f"EV_{datetime.now().strftime("%H:%M")}"
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate
        self.tournament_size = tournament_size

        self.generation = 0
        self.population = []
        self.best_agent = None
        self.best_points_agent = None
        self.average_fitness = 0
        self.fitness_standard_deviation = 0
        self.average_points = 0
        self.points_standard_deviation = 0

        self.generator = np.random.default_rng(seed)
        
        self.save_population_data(seed)



    def create_new_population(self, game_size):
        self.generation += 1
        # create folder "data" if not exists
        Path("data").mkdir(parents=True, exist_ok=True)
        # create folder "data/generation_1" if not exists
        Path(f"data/generation_{self.generation}").mkdir(parents=True, exist_ok=True)
        for i in range(self.population_size):
            self.population.append(Agent("Agent-" + str(i), game_size, generator=self.generator))
            

    def breed_population(self):
        self.generation += 1
        self.selection()
        # create folder "data/generation_n" if not exists
        Path(f"data/generation_{self.generation}").mkdir(parents=True, exist_ok=True)
        # update names of agents
        for i, agent in enumerate(self.population):
            agent.name = "Agent-" + str(i)
            agent.fitness = 0


    def selection(self):
        parents = []
        parents += self.elitism_selection()
        random.shuffle(parents)

        new_population = []
        new_population += self.elitism_selection()

        while len(new_population) < self.population_size:
            parent1 = self.roulette_selection(parents)
            parent2 = self.roulette_selection(parents)
            offspring = self.crossover(parent1, parent2).mutate(self.mutation_rate)
            new_population.append(offspring)
        
        self.population = new_population


    def elitism_selection(self):
        # choose elite agents first
        best_agents = []
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        for i in range(int(self.population_size * self.elitism_rate)):
            best_agents.append(self.population[i].clone())
        return best_agents


    def parent_selection(self):
        best_agents = []
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        for i in range(int(self.population_size / 2)):
            best_agents.append(self.population[i])
        return best_agents


    def tournament_selection(self):
        # choose random agents from population
        tournament_size = int(self.tournament_size * self.population_size)
        tournament = []
        for i in range(tournament_size):
            tournament.append(self.population[random.randint(0, self.population_size - 1)])
        # choose best agent from tournament
        tournament.sort(key=lambda x: x.fitness, reverse=True)
        return tournament[0]
    

    def roulette_selection(self, agents):
        # choose random agents from population
        total_score = sum([agent.fitness for agent in agents])
        pick = random.uniform(0, total_score)
        current = 0
        for agent in agents:
            current += agent.fitness
            if current > pick:
                return agent
        return agents[-1]


    def crossover(self, agent1, agent2):
        new_agent = Agent(agent1.name, agent1.game_size, generator=self.generator)
        for i in range(new_agent.input_size):
            for j in range(new_agent.hidden_size):
                if random.random() < 0.5:
                    new_agent.W1[i][j] = agent1.W1[i][j]
                else:
                    new_agent.W1[i][j] = agent2.W1[i][j]
        for i in range(new_agent.hidden_size):
            for j in range(new_agent.second_hidden_size):
                if random.random() < 0.5:
                    new_agent.W2[i][j] = agent1.W2[i][j]
                else:
                    new_agent.W2[i][j] = agent2.W2[i][j]
        for i in range(new_agent.second_hidden_size):
            for j in range(new_agent.output_size):
                if random.random() < 0.5:
                    new_agent.W3[i][j] = agent1.W3[i][j]
                else:
                    new_agent.W3[i][j] = agent2.W3[i][j]
        return new_agent
    

    def one_point_crossover(self, agent1, agent2):
        new_agent = Agent(agent1.name, agent1.game_size, generator=self.generator)
        w1_point = random.randint(0, new_agent.input_size - 1)
        w2_point = random.randint(0, new_agent.hidden_size - 1)
        w3_point = random.randint(0, new_agent.hidden_size - 1)
        for i in range(new_agent.input_size):
            for j in range(new_agent.hidden_size):
                if i < w1_point:
                    new_agent.W1[i][j] = agent1.W1[i][j]
                else:
                    new_agent.W1[i][j] = agent2.W1[i][j]
        for i in range(new_agent.hidden_size):
            for j in range(new_agent.hidden_size):
                if i < w2_point:
                    new_agent.W2[i][j] = agent1.W2[i][j]
                else:
                    new_agent.W2[i][j] = agent2.W2[i][j]
        for i in range(new_agent.hidden_size):
            for j in range(new_agent.output_size):
                if i < w3_point:
                    new_agent.W3[i][j] = agent1.W3[i][j]
                else:
                    new_agent.W3[i][j] = agent2.W3[i][j]
        return new_agent
    
    def select_best_agent(self):
        best_fitness = -1_000_000
        self.best_agent = None
        for agent in self.population:
            if agent.fitness > best_fitness:
                self.best_agent = agent
                best_fitness = agent.fitness
        if self.best_agent == None:
            self.best_agent = self.population[0]


    def select_best_points(self):
        best_points = 0
        self.best_points_agent = None
        for agent in self.population:
            if agent.points > best_points:
                self.best_points_agent = agent
                best_points = agent.points
        if self.best_points_agent == None:
            self.best_points_agent = self.population[0]


    def get_population_fitness_avg(self):
        return sum([agent.fitness for agent in self.population]) / self.population_size


    def get_fitness_standard_deviation(self):
        avg = self.get_population_fitness_avg()
        return (sum([(agent.fitness - avg) ** 2 for agent in self.population]) / self.population_size) ** 0.5
    

    def get_population_points_avg(self):
        return sum([agent.points for agent in self.population]) / self.population_size
    

    def get_points_standard_deviation(self):
        avg = self.get_population_points_avg()
        return (sum([(agent.points - avg) ** 2 for agent in self.population]) / self.population_size) ** 0.5
    

    def calculate_generation_stats(self):
        self.average_fitness = self.get_population_fitness_avg()
        self.fitness_standard_deviation = self.get_fitness_standard_deviation()
        self.average_points = self.get_population_points_avg()
        self.points_standard_deviation = self.get_points_standard_deviation()


    def calculate_best_points_and_score(self):
        self.select_best_points()
        self.select_best_agent()


    def save_population_data(self, seed):
        Path("population_data").mkdir(parents=True, exist_ok=True)
        with open(f"population_data/{self.name}.txt", "w") as f:
            f.write(f"{self.population_size}, {self.mutation_rate}, {self.elitism_rate}, {seed}\n")


    def save_generation_data(self):
        self.calculate_generation_stats()
        with open(f"population_data/{self.name}.txt", "a") as f:
            f.write(f"{self.generation}, {round(self.average_fitness, 2)}, {round(self.fitness_standard_deviation, 2)}, {round(self.average_points, 2)}, {round(self.points_standard_deviation, 2)}, {self.best_agent.fitness}, {self.best_agent.points}, {self.best_agent.name}\n")


    def get_actual_generation_data(self):
        self.calculate_generation_stats()
        return [self.generation, round(self.average_fitness, 2), round(self.fitness_standard_deviation, 2), round(self.average_points, 2),
                 round(self.points_standard_deviation, 2), self.best_agent.fitness, self.best_agent.points, self.best_agent.name]
    

    def load_population_data(self, path, generation):
        new_population = []
        self.generation = generation
        for i in range(self.population_size):
            agent = Agent("Agent-" + str(i), (10, 10), generator=self.generator)
            agent.load_brain(f"{path}/Agent-{i}/brain")
            new_population.append(agent)
        self.population = new_population
        
        # create folder "data" if not exists
        Path("data").mkdir(parents=True, exist_ok=True)
        # create folder "data/generation_1" if not exists
        Path(f"data/generation_{self.generation}").mkdir(parents=True, exist_ok=True)