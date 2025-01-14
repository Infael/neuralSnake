from .game.SnakeGame import SnakeGame
from .ai.Evolution import Evolution
from .stats.EvolutionPlot import EvolutionPlotter
import time
from pathlib import Path
import random
import os


GENERATIONS = 500
POPULATION_SIZE = 500
MUTATION_RATE = 0.2
ELITISM_RATE = 0.002
SEED = 42
GAMES_COUNT_FOR_EACH_AGENT_IN_EACH_GENERATION = 3

random.seed(SEED)

def main(generationFile = None, generation = 0):
    game_size = (10, 10)
    
    evolution = Evolution(population_size=POPULATION_SIZE, mutation_rate=MUTATION_RATE, elitism_rate=ELITISM_RATE, seed=SEED)
    if generationFile:
        evolution.load_population_data(generationFile, generation)
        print("Loaded population data")
    else:
        evolution.create_new_population(game_size)
    plot = EvolutionPlotter(evolution.name, real_time=True)

    while evolution.generation <= GENERATIONS:
        start_generation = time.time()
        for agent in evolution.population:
            Path(f"data_{MUTATION_RATE}_{ELITISM_RATE}/generation_{evolution.generation}/{agent.name}").mkdir(parents=True, exist_ok=True)
            agent.save_brain(f"data_{MUTATION_RATE}_{ELITISM_RATE}/generation_{evolution.generation}/{agent.name}/brain")
            # Every agent will play n games
            best_points = 0
            average_points = 0
            average_steps = 0
            for i in range(GAMES_COUNT_FOR_EACH_AGENT_IN_EACH_GENERATION):
                game = SnakeGame(f"data_{MUTATION_RATE}_{ELITISM_RATE}/generation_{evolution.generation}/{agent.name}/game-{i}", game_size, 101)
                alive, points, steps = game.move(agent.get_next_move(game.get_game_state()))
                while alive:
                    alive, points, steps = game.move(agent.get_next_move(game.get_game_state()))
                game.save_game_replay_data()
                if points > best_points:
                    best_points = points
                average_points += points
                average_steps += steps

            average_points /= GAMES_COUNT_FOR_EACH_AGENT_IN_EACH_GENERATION
            average_steps /= GAMES_COUNT_FOR_EACH_AGENT_IN_EACH_GENERATION
            agent.calculate_fitness(average_points, average_steps)
            agent.points = best_points

        evolution.calculate_best_points_and_score()
        evolution.save_generation_data()
        # plot.add_data(evolution.get_actual_generation_data())
        # plot.plot_data_real_time()
        
        print(f"Generation: {evolution.generation}, Generation Average: {evolution.average_fitness}\nBest Fitness: {evolution.best_agent.fitness}, Best Points: {evolution.best_agent.points}, Best Agent: {evolution.best_agent.name}")
        evolution.breed_population()
        print("Time taken", round(time.time() - start_generation, 2), "seconds", "Estimated time left",  round((time.time() - start_generation) * (GENERATIONS - evolution.generation) / 60, 2), "minutes")
        print("----------------------------------------")



if __name__ == "__main__":
    try:
        main(os.sys.argv[1], int(os.sys.argv[2]))
    except IndexError:
        print("No generation file provided")
        main()
    