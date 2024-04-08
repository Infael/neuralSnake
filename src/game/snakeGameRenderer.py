import tkinter as tk
import os
from model import SnakeGameState
      

class SnakeGameRenderer:
    def __init__(self, file_name):
       self.file_name = file_name
       self.root = tk.Tk()
       self.root.title("Snake Game")
       self.canvas = tk.Canvas(self.root, width=200, height=200)
       self.game_states = []
       self.load_snake_game()
       self.canvas.pack()
       self.render()
       self.gameloop()
       self.root.mainloop()

    
    def update_canvas_size(self, size):
      size = size.split(",")
      self.canvas.config(width=int(size[0])*10, height=int(size[1])*10)

    def load_snake_game(self):
      with open(self.file_name, "r") as f:
        lines = f.readlines()
        self.update_canvas_size(lines.pop(0))
        for i in range(0, len(lines), 3):
          snake = eval(lines[i])
          food = eval(lines[i+1])
          score = lines[i+2]
          game_state = SnakeGameState.SnakeGameState(snake, food, score)
          self.game_states.append(game_state)

    def gameloop(self):
      self.render()
      self.root.after(100, self.gameloop)
    
    def render(self):
      if not self.game_states:
        return
      self.canvas.delete("all")
      game_state = self.game_states.pop(0)
      for segment in game_state.snake:
        self.canvas.create_rectangle(segment[0]*10, segment[1]*10, segment[0]*10 + 10, segment[1]*10 + 10, fill="lime")
      self.canvas.create_rectangle(game_state.food[0]*10, game_state.food[1]*10, game_state.food[0]*10 + 10, game_state.food[1]*10 + 10, fill="red")
      self.canvas.create_text(10, 10, text=f"Score: {game_state.score}", anchor="nw")
        

def main(file_name):
    SnakeGameRenderer(file_name)


if __name__ == "__main__":
  file_name = os.sys.argv[1]
  if not file_name:
    print("Usage: python snakeGameRenderer.py <file_name>")
    exit(1)
  main(file_name)