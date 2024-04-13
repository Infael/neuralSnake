import random
from .model.SnakeGameState import SnakeGameState

GAME_WIDTH = 20
GAME_HEIGHT = 20

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class SnakeGame:
  def __init__(self, game_name, game_size = (GAME_WIDTH, GAME_HEIGHT), max_steps = 100): 
    self.game_name = game_name
    self.points = 0
    self.steps = 0
    self.width = game_size[0]
    self.height = game_size[1]
    self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    self.head_positions = []
    self.initial_snake = []
    self.food_positions = []
    self.create_snake()
    self.food = self.generate_food()
    self.snake_life = max_steps
    self.max_life = max_steps

    

  def create_snake(self):
    self.snake = [[self.width // 2, self.height // 2]]
    # append 2 tail parts based on the direction
    if self.direction == UP:
      self.snake.append([self.width // 2, self.height // 2 + 1])
      self.snake.append([self.width // 2, self.height // 2 + 2])
    elif self.direction == DOWN:
      self.snake.append([self.width // 2, self.height // 2 - 1])
      self.snake.append([self.width // 2, self.height // 2 - 2])
    elif self.direction == LEFT:
      self.snake.append([self.width // 2 + 1, self.height // 2])
      self.snake.append([self.width // 2 + 2, self.height // 2])
    elif self.direction == RIGHT:
      self.snake.append([self.width // 2 - 1, self.height // 2])
      self.snake.append([self.width // 2 - 2, self.height // 2])
    self.initial_snake = self.snake.copy()
    

  def generate_food(self):
    generated = False
    while not generated:
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - 1)
      if [x, y] not in self.snake:
        generated = True
        self.food_positions.append([x, y])
        return [x, y]


  def move(self, direction):
    head = self.snake[0]
    new_head = []
    
    if direction == UP and self.direction != DOWN:
      new_head = [head[0], head[1] - 1]
      self.direction = UP
    elif direction == DOWN and self.direction != UP:
      new_head = [head[0], head[1] + 1]
      self.direction = DOWN
    elif direction == LEFT and self.direction != RIGHT:
      new_head = [head[0] - 1, head[1]]
      self.direction = LEFT
    elif direction == RIGHT and self.direction != LEFT:
      new_head = [head[0] + 1, head[1]]
      self.direction = RIGHT
    else:
      return self.move(self.direction)

    if new_head == self.food:
      self.points += 1
      self.snake_life = self.max_life
      self.snake.insert(0, new_head)
      self.food = self.generate_food()
    else:
      self.snake_life -= 1
      self.snake.insert(0, new_head)
      self.snake.pop()
    
    self.steps += 1
    self.head_positions.append(new_head)

    if self.is_game_over():
      return (False, self.points, self.steps)
    else:
      return (True, self.points, self.steps)


  def is_game_over(self):
    head = self.snake[0]
    if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
      return True
    if head in self.snake[1:]:
      return True
    if self.snake_life <= 0:
      return True
    return False
  
  # Not used anywhere, I was just trying to make better fitness function
  def calculate_average_distance_to_food(self):
    head = self.snake[0]
    distance = abs(head[0] - self.food[0]) + abs(head[1] - self.food[1])
    self.average_distance_to_food = (self.average_distance_to_food * (self.steps - 1) + distance) / self.steps

  
  def get_game_state(self):
    return SnakeGameState(self.snake, self.food, self.points, self.snake_life, self.direction)
  

  def get_game_size(self):
    return self.width, self.height


  def save_game_replay_data(self):
    with open(self.game_name, "w") as f:
      f.write(f"{self.width}, {self.height}, {self.max_life}, {self.points}, {self.snake_life}\n")
      f.write(f"{self.initial_snake}\n")
      f.write(f"{self.head_positions}\n")
      f.write(f"{self.food_positions}\n")



def main():
  game = SnakeGame("testGame")
  game_over = False
  while not game_over:
    game_state = game.get_game_state()
    print(game_state)
    direction = input("Enter direction: ")
    game_over = not game.move(int(direction))[0]

  print("Game Over")
  print("Score: ", game.points)


if __name__ == "__main__":
  main()