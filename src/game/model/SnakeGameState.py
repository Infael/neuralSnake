class SnakeGameState:
    def __init__(self, snake, food, score, life, direction):
      self.snake = snake
      self.food = food
      self.score = score
      self.snake_life = life
      self.direction = direction # UP, DOWN, LEFT, RIGHT - 0, 1, 2, 3

    def __str__(self):
      return f"Snake: {self.snake}, Food: {self.food}, Score: {self.score}, Life: {self.snake_life}"