import random

GAME_WIDTH = 20
GAME_HEIGHT = 20


random.seed(42)

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class SnakeGame:
  def __init__(self, game_name): 
    self.game_name = game_name
    self.score = 0
    self.width = GAME_WIDTH
    self.height = GAME_HEIGHT
    self.snake = [[GAME_WIDTH // 2, GAME_HEIGHT // 2]]
    self.food = self.generate_food()

    with open(self.game_name, "w") as f:
      f.write(f"{self.width}, {self.height}\n")
    self.save_game_state()
    

  def generate_food(self):
    generated = False
    while not generated:
      x = random.randint(0, self.width - 1)
      y = random.randint(0, self.height - 1)
      if [x, y] not in self.snake:
        generated = True
        return [x, y]

  def get_game_state(self):
    return self.snake, self.food, self.score

  def move(self, direction):
    head = self.snake[0]
    new_head = []
    if direction == UP:
      new_head = [head[0], head[1] - 1]
    elif direction == DOWN:
      new_head = [head[0], head[1] + 1]
    elif direction == LEFT:
      new_head = [head[0] - 1, head[1]]
    elif direction == RIGHT:
      new_head = [head[0] + 1, head[1]]

    if new_head == self.food:
      self.score += 1
      self.snake.insert(0, new_head)
      self.food = self.generate_food()
    else:
      self.snake.insert(0, new_head)
      self.snake.pop()

    self.save_game_state()

    if self.is_game_over():
      return False
    else:
      return True

  def is_game_over(self):
    head = self.snake[0]
    if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
      return True

    if head in self.snake[1:]:
      return True

    return False

  def save_game_state(self):
    with open(self.game_name, "a") as f:
      f.write(f"{self.snake}\n")
      f.write(f"{self.food}\n")
      f.write(f"{self.score}\n")

def main():
  game = SnakeGame("testGame")
  game_over = False
  while not game_over:
    game_state = game.get_game_state()
    print(game_state)
    direction = input("Enter direction: ")
    game_over = not game.move(int(direction))

  print("Game Over")
  print("Score: ", game.score)


if __name__ == "__main__":
  main()