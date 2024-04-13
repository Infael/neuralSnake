import tkinter as tk
import os
from .model.SnakeGameState import SnakeGameState


PADDING_GAME = 20
PADDING_GAME_LEFT = 60
      

class SnakeGameRenderer:
    def __init__(self, file_name, old = False):
      self.file_name = file_name
      self.root = tk.Tk()
      self.root.title("Snake Game")
      self.canvas = tk.Canvas(self.root, width=200, height=200)
      self.snake = []
      self.head_positions = []
      self.food_positions = []
      
      # old
      self.old = old
      self.game_states = []
      
      self.width = 0
      self.height = 0

      self.max_life = 0
      self.points = 0
      self.actual_life = 0

      if self.old:
        self.load_snake_game_old()
      else:
        self.load_snake_game()
      self.canvas.pack()
      self.gameloop()
      self.root.mainloop()

    
    def update_canvas_size(self, size):
      size = size.split(",")
      self.width = int(size[0])
      self.height = int(size[1])
      self.canvas.config(width=int(size[0])*10 + 2*PADDING_GAME + PADDING_GAME_LEFT, height=int(size[1])*10 + 2*PADDING_GAME)


    def load_snake_game(self):
      with open(self.file_name, "r") as f:
        lines = f.readlines()
        # first line is the size of the game
        first_line = lines.pop(0)
        self.max_life = int(first_line.split(",")[2])
        self.actual_life = self.max_life
        self.update_canvas_size(first_line)
        # second line is initial position of a snake
        self.snake = eval(lines.pop(0))
        # third line is all head positions of a snake during the game
        self.head_positions = eval(lines.pop(0))
        # fourth line is all food positions of a snake during the game
        self.food_positions = eval(lines.pop(0))
         
    def load_snake_game_old(self):
      with open(self.file_name, "r") as f:
        lines = f.readlines()
        self.update_canvas_size(lines.pop(0))
        for i in range(0, len(lines), 3):
          snake = eval(lines[i])
          food = eval(lines[i+1])
          score, life = lines[i+2].split(",")
          game_state = SnakeGameState(snake, food, score, life, 0)
          self.game_states.append(game_state)

    def gameloop(self):
      if (not self.old):
        self.update()
        self.render()
      else:
        self.render_old()
      self.root.after(100, self.gameloop)
    

    def update(self):
      if not self.head_positions:
        return
      head_position = self.head_positions.pop(0)
      self.snake.insert(0, head_position)
      if self.snake[0] == self.food_positions[0]:
        self.points += 1
        self.actual_life = self.max_life
        self.food_positions.pop(0)
      else:
        self.snake.pop()
        self.actual_life -= 1
      
    def render_old(self):
      if not self.game_states:
        return
      self.canvas.delete("all")
      game_state = self.game_states.pop(0)
      for segment in game_state.snake:
        self.canvas.create_rectangle(segment[0]*10 + PADDING_GAME + PADDING_GAME_LEFT, segment[1]*10 + PADDING_GAME, segment[0]*10 + 10 + PADDING_GAME + PADDING_GAME_LEFT, segment[1]*10 + 10 + PADDING_GAME, fill="lime")
      self.canvas.create_rectangle(game_state.food[0]*10 + PADDING_GAME + PADDING_GAME_LEFT, game_state.food[1]*10 + PADDING_GAME, game_state.food[0]*10 + 10 + PADDING_GAME + PADDING_GAME_LEFT, game_state.food[1]*10 + 10 + PADDING_GAME, fill="red")
      self.canvas.create_text(10, 10, text=f"Score: {game_state.score}", anchor="nw")
      self.canvas.create_text(10, 25, text=f"Life: {game_state.snake_life}", anchor="nw")
      self.render_border()

    def render(self):
      self.canvas.delete("all")
      for i, segment in enumerate(self.snake):
        if i == 0:
          self.canvas.create_rectangle(segment[0]*10 + PADDING_GAME + PADDING_GAME_LEFT, segment[1]*10 + PADDING_GAME, segment[0]*10 + 10 + PADDING_GAME + PADDING_GAME_LEFT, segment[1]*10 + 10 + PADDING_GAME, fill="green")
        else:
          self.canvas.create_rectangle(segment[0]*10 + PADDING_GAME + PADDING_GAME_LEFT, segment[1]*10 + PADDING_GAME, segment[0]*10 + 10 + PADDING_GAME + PADDING_GAME_LEFT, segment[1]*10 + 10 + PADDING_GAME, fill="lime")
      self.canvas.create_rectangle(self.food_positions[0][0]*10 + PADDING_GAME + PADDING_GAME_LEFT, self.food_positions[0][1]*10 + PADDING_GAME, self.food_positions[0][0]*10 + 10 + PADDING_GAME + PADDING_GAME_LEFT, self.food_positions[0][1]*10 + 10 + PADDING_GAME, fill="red")
      self.canvas.create_text(10, 10, text=f"Score: {self.points}", anchor="nw")
      self.canvas.create_text(10, 25, text=f"Life: {self.actual_life}", anchor="nw")
      self.render_border()

    def render_border(self):
      self.canvas.create_rectangle(PADDING_GAME + PADDING_GAME_LEFT, PADDING_GAME, self.width*10 + PADDING_GAME + PADDING_GAME_LEFT, self.height*10 + PADDING_GAME, outline="white")

def main(file_name, old = False):
    SnakeGameRenderer(file_name, old)


if __name__ == "__main__":
  file_name = os.sys.argv[1]
  old_file = ""
  try:
    old_file = os.sys.argv[2]
  except IndexError:
    pass
  if old_file == "old":
    main(file_name, True)
  
  if not file_name:
    print("Usage: python snakeGameRenderer.py <file_name>")
    exit(1)
  main(file_name)