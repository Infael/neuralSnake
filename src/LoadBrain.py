import os
from src.game.SnakeGame import SnakeGame
from src.game.SnakeGameRenderer import SnakeGameRenderer
from src.ai.Agent import Agent


def main(brain_file, map_size = 10):
    game_size = (map_size, map_size)

    game = SnakeGame("loadedBrainGame", game_size)
    agent = Agent("loadedBrain", game_size)
    agent.load_brain(brain_file)
    alive, points, steps = game.move(agent.get_next_move(game.get_game_state()))
    while alive:
        alive, points, steps = game.move(agent.get_next_move(game.get_game_state()))
    game.save_game_replay_data()

    SnakeGameRenderer("loadedBrainGame")



if __name__ == "__main__":
    brain_file = os.sys.argv[1]
    map_size = int(os.sys.argv[2])
    main(brain_file, map_size)