# NEURAL SNAKE

The project consists of a game, an evolutionary algorithm and a neural network.
The neural network learns to play the game Snake using the evolutionary algorithm.

### Game

The game can only be played on a console (AI agents don§t need to see the game). The game is saved in a specified file and can be rendered using the snakeGameRenderer.py file. Life of the snake is limited and is reseted after picking food (to eliminate cycled snakes).

### Neural Network

The neural network consists of 28 input neurons, 2 hidden layers and one output layer. The input layers consist of 3x8 neurons for vision (8 directions, looking for apple, tail or wall in each direction) and 4 binary neurons for the direction of the snake. The vision neurons for the apple and tail could also be binary (it doesn't seem to change anything significantly). The hidden layers have 20 and 12 neurons (because reasons??), and the output layer consists of 4 neurons for the next direction of the snake. Activation function of neurons is ReLU on hidden layers and sigmoid on output layer.

Fitness of an agent is calculated like this: (it is trying to reward long-lived snakes earlier and more points later (and it is working))

```python
fitness = steps + (2**points + (points**2.1) * 500) - ((points**1.2) * ((0.25 * steps)**1.3))
```

### Evolution Algorithm

Evolution algorithm consist of population of specific size, mutation rate, elitism (with editable rate). By default for selection is used roulette selection. Can be changed for implemented tournament selection. There is also parameter for tournament size. All mentioned values can be changed in main.py file. For crossover is curently used crossover for each weight in layer. Can be also switched for implemented one-point crossover, but I didn't tried it much.

## Install dependencies

```bash
  conda create --name neuralSnake
  conda activate neuralSnake
  conda env update --file environment.yml
```

## Usage

To start the evolution

```bash
  python -m src.main
```

To load specific generation to continue evolution

```bash
  python -m src.main <path_to_generation_data> <generation_id>
```

To load specific trained brain for playing

```bash
  python -m src.LoadBrain <path_to_brain_files_ending_with_"/brain"> <map_size>
```

To visualize played game

```bash
  python -m src.game.SnakeGameRenderer <path_to_game_data>
```

To render plot of evolution (file probably from generated population_data dir)

```bash
  python -m src.stats.EvolutionPlot <file_name>
```

### Project is using:

- numpy
- matplotlib

### Other notes

- You can also specify seed for random number generation to make results repeatable.
- I kept **/best_brains** directory here. It has agent that reached 42 points in a 10 by 10 map. That's almost half of the map. I'm so proud of my boy! (But I saved him in a wrong format so there is also python file to convert him to npy format) (It's agent 415) (also his games are in an old format, but you can play show them with SnakeGameRenderer and flag old)

