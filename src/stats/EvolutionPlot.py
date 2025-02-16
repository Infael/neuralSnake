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
        # plot standard deviation as a shaded area
        plt.fill_between(self.generation, [x - y for x, y in zip(self.average_points, self.points_standard_deviation)],
         [x + y for x, y in zip(self.average_points, self.points_standard_deviation)], alpha=0.4, label="Standard Deviation", facecolor=(0,.9,.2,.6))
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

class EvolutionStats:
    def __init__(self, filename):
        self.name = filename
        self.bestPoints = None
        self.bestPointsGeneration = None
        self.bestPointsAgent = None
        self.bestAveragePoints = None
        self.bestAveragePointsGeneration = None

        self.lastGenerationBestPoints = None
        self.lastGenerationBestPointsAgent = None
        self.lastGenerationAveragePoints = None
        self.read_data(filename)
        self.print_data()

    def read_data(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                data = line.split(",")
                if self.bestPoints == None or float(data[6]) > self.bestPoints:
                    self.bestPoints = float(data[6])
                    self.bestPointsGeneration = int(data[0])
                    self.bestPointsAgent = data[7]
                if self.bestAveragePoints == None or float(data[3]) > self.bestAveragePoints:
                    self.bestAveragePoints = float(data[3])
                    self.bestAveragePointsGeneration = int(data[0])
            self.lastGenerationBestPoints = float(lines[-1].split(",")[6])
            self.lastGenerationAveragePoints = float(lines[-1].split(",")[3])
            self.lastGenerationBestPointsAgent = lines[-1].split(",")[7]
    
    def print_data(self):
        print(f"Best Points: {self.bestPoints} in Generation {self.bestPointsGeneration} by Agent {self.bestPointsAgent}")
        print(f"Best Average Points: {self.bestAveragePoints} in Generation {self.bestAveragePointsGeneration}")
        print(f"Last Generation Best Points: {self.lastGenerationBestPoints} by Agent {self.lastGenerationBestPointsAgent}")
        print(f"Last Generation Average Points: {self.lastGenerationAveragePoints} ")
        

def main(file_name):
    EvolutionStats(file_name)
    evolution_data = EvolutionPlotter(file_name)
    evolution_data.read_data(file_name)
    # evolution_data.plot_fitness()
    evolution_data.plot_points()

        

if __name__ == "__main__":
    file_name = os.sys.argv[1]
    if not file_name:
        print("Usage: python snakeGameRenderer.py <file_name>")
        exit(1)
    main(file_name)





