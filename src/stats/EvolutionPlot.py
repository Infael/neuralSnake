import os
from matplotlib import pyplot as plt



class EvolutionPlotter:
    def __init__(self, filename, real_time=False):
        self.name = filename
        self.generation = []
        self.average_fitness = []
        self.fitness_standard_deviation = []
        self.average_points = []
        self.points_standard_deviation = []
        self.best_agent_score = []
        self.best_agent_points = []
        self.best_agent_name = []

        if real_time:
            plt.ion()   
            self.fig, self.ax = plt.subplots()
            self.line_average = self.ax.plot([], [], label="Average Score")[0]
            self.line_best_points = self.ax.plot([], [], label="Best Score")[0]
            self.line_standard_deviation = self.ax.plot([], [], label="Standard Deviation")[0]
        
            plt.legend()    
        

    def read_data(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                data = line.split(",")
                self.generation.append(int(data[0]))
                self.average_fitness.append(float(data[1]))
                self.fitness_standard_deviation.append(float(data[2]))
                self.average_points.append(float(data[3]))
                self.points_standard_deviation.append(float(data[4]))
                self.best_agent_score.append(float(data[5]))
                self.best_agent_points.append(float(data[6]))
                self.best_agent_name.append(data[7])

    def add_data(self, data):
        self.generation.append(int(data[0]))
        self.average_fitness.append(float(data[1]))
        self.fitness_standard_deviation.append(float(data[2]))
        self.average_points.append(float(data[3]))
        self.points_standard_deviation.append(float(data[4]))
        self.best_agent_score.append(float(data[5]))
        self.best_agent_points.append(float(data[6]))
        self.best_agent_name.append(data[7])

    def create_plot_fitness(self):
        plt.plot(self.generation, self.best_agent_score, label="Best Score")
        plt.plot(self.generation, self.average_fitness, label="Average Score")
        plt.plot(self.generation, self.fitness_standard_deviation, label="Standard Deviation")
        plt.legend()

    def create_plot_points(self):
        plt.plot(self.generation, self.best_agent_points, label="Best Points")
        plt.plot(self.generation, self.average_points, label="Average Points")
        plt.plot(self.generation, self.points_standard_deviation, label="Standard Deviation")
        plt.legend()
        
    def plot_fitness(self):
        self.create_plot_fitness()
        plt.show()

    def plot_points(self):
        self.create_plot_points()
        plt.show()

    def plot_data_real_time(self):
        self.line_average.set_xdata(self.generation)
        self.line_average.set_ydata(self.average_points)
        self.line_best_points.set_xdata(self.generation)
        self.line_best_points.set_ydata(self.best_agent_points)
        self.line_standard_deviation.set_xdata(self.generation)
        self.line_standard_deviation.set_ydata(self.points_standard_deviation)
        

        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def main(file_name):
    evolution_data = EvolutionPlotter(file_name)
    evolution_data.read_data(file_name)
    evolution_data.plot_fitness()
    evolution_data.plot_points()
        

if __name__ == "__main__":
    file_name = os.sys.argv[1]
    if not file_name:
        print("Usage: python snakeGameRenderer.py <file_name>")
        exit(1)
    main(file_name)





