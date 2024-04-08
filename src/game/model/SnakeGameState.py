class SnakeGameState:
    def __init__(self, snake, food, score):
      self.snake = snake
      self.food = food
      self.score = score

    def __str__(self):
      return f"Snake: {self.snake}, Food: {self.food}, Score: {self.score}"