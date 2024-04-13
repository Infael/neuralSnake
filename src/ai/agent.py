import numpy as np
from ..game.model.SnakeGameState import SnakeGameState

# Snake Agent with 8x3 input and 4 output
# 8x3 input: 8 directions, 3 possible v alues (if he sees walls, food or snake) + 4 direction of movement
# 4 output: 4 possible directions for the next move
# 2 x 18 neurons in hidden layers (2 layers)

BIAS = 0
FOOD_AND_TAIL_VISION_BINARY = True

class Agent:
    def __init__(self, agent_name, game_size, generator = None):
        self.name = agent_name
        self.game_size = game_size
        self.fitness = 0
        self.points = 0

        if generator is None:
            self.generator = np.random.default_rng()
        else:
            self.generator = generator

        self.input_size = 8 * 3 + 4
        # Hidden layers can be adjusted
        self.hidden_size = 20
        self.second_hidden_size = 12
        self.output_size = 4
        self.W1 = self.generator.uniform(-1, 1, (self.input_size + 1, self.hidden_size))
        self.W2 = self.generator.uniform(-1, 1, (self.hidden_size + 1, self.second_hidden_size))
        self.W3 = self.generator.uniform(-1, 1, (self.second_hidden_size + 1, self.output_size))

    # I know this is a long function, but it is just a bunch of if statements
    def parse_input(self, inputData: SnakeGameState):
        parsedInput = np.zeros((8, 3))
        # get the snake head
        head = inputData.snake[0]
        # look to each direction and find out if there is a food, wall or add distance to wall
        # 8 directions: up, down, left, right, up-left, up-right, down-left, down-right

        # UP
        up = [head[0], head[1] - 1]
        while up[1] >= 0:
            if up in inputData.snake and parsedInput[0][1] == 0:
                parsedInput[0][1] = 1 if FOOD_AND_TAIL_VISION_BINARY else head[1]
            if up == inputData.food:
                parsedInput[0][0] = 1 if FOOD_AND_TAIL_VISION_BINARY else head[1]
            up[1] -= 1
        if up[1] < 0:
            parsedInput[0][2] = head[1]
        # DOWN
        down = [head[0], head[1] + 1]
        while down[1] < self.game_size[1]:
            if down in inputData.snake and parsedInput[1][1] == 0:
                parsedInput[1][1] = 1 if FOOD_AND_TAIL_VISION_BINARY else self.game_size[1] - head[1] - 1
            if down == inputData.food:
                parsedInput[1][0] = 1 if FOOD_AND_TAIL_VISION_BINARY else self.game_size[1] - head[1] - 1
            down[1] += 1
        if down[1] >= self.game_size[1]:
            parsedInput[1][2] = self.game_size[1] - head[1] - 1
        # LEFT
        left = [head[0] - 1, head[1]]
        while left[0] >= 0:
            if left in inputData.snake and parsedInput[2][1] == 0:
                parsedInput[2][1] = 1 if FOOD_AND_TAIL_VISION_BINARY else head[0]
            if left == inputData.food:
                parsedInput[2][0] = 1 if FOOD_AND_TAIL_VISION_BINARY else head[0]
            left[0] -= 1
        if left[0] < 0:
            parsedInput[2][2] = head[0]
        # RIGHT
        right = [head[0] + 1, head[1]]
        while right[0] < self.game_size[0]:
            if right in inputData.snake and parsedInput[3][1] == 0:
                parsedInput[3][1] = 1 if FOOD_AND_TAIL_VISION_BINARY else self.game_size[0] - head[0] - 1
            if right == inputData.food:
                parsedInput[3][0] = 1 if FOOD_AND_TAIL_VISION_BINARY else self.game_size[0] - head[0] - 1
            right[0] += 1
        if right[0] >= self.game_size[0]:
            parsedInput[3][2] = self.game_size[0] - head[0] - 1
        # UP-LEFT
        up_left = [head[0] - 1, head[1] - 1]
        distance = 0
        while up_left[0] >= 0 and up_left[1] >= 0:
            distance += 1
            if up_left in inputData.snake and parsedInput[4][1] == 0:
                parsedInput[4][1] = 1 if FOOD_AND_TAIL_VISION_BINARY else distance
            if up_left == inputData.food:
                parsedInput[4][0] = 1 if FOOD_AND_TAIL_VISION_BINARY else distance
            up_left[0] -= 1
            up_left[1] -= 1
        if up_left[0] < 0 or up_left[1] < 0:
            parsedInput[4][2] = distance
        # UP-RIGHT
        up_right = [head[0] + 1, head[1] - 1]
        distance = 0
        while up_right[0] < self.game_size[0] and up_right[1] >= 0:
            distance += 1
            if up_right in inputData.snake and parsedInput[5][1] == 0:
                parsedInput[5][1] = 1 if FOOD_AND_TAIL_VISION_BINARY else distance
            if up_right == inputData.food:
                parsedInput[5][0] = 1 if FOOD_AND_TAIL_VISION_BINARY else distance
            up_right[0] += 1
            up_right[1] -= 1
        if up_right[0] >= self.game_size[0] or up_right[1] < 0:
            parsedInput[5][2] = distance
        # DOWN-LEFT
        down_left = [head[0] - 1, head[1] + 1]
        distance = 0
        while down_left[0] >= 0 and down_left[1] < self.game_size[1]:
            distance += 1
            if down_left in inputData.snake and parsedInput[6][1] == 0:
                parsedInput[6][1] = 1 if FOOD_AND_TAIL_VISION_BINARY else distance
            if down_left == inputData.food:
                parsedInput[6][0] = 1 if FOOD_AND_TAIL_VISION_BINARY else distance
            down_left[0] -= 1
            down_left[1] += 1
        if down_left[0] < 0 or down_left[1] >= self.game_size[1]:
            parsedInput[6][2] = distance
        # DOWN-RIGHT
        down_right = [head[0] + 1, head[1] + 1]
        distance = 0
        while down_right[0] < self.game_size[0] and down_right[1] < self.game_size[1]:
            distance += 1
            if down_right in inputData.snake and parsedInput[7][1] == 0:
                parsedInput[7][1] = 1 if FOOD_AND_TAIL_VISION_BINARY else distance
            if down_right == inputData.food:
                parsedInput[7][0] = 1 if FOOD_AND_TAIL_VISION_BINARY else distance
            down_right[0] += 1
            down_right[1] += 1
        if down_right[0] >= self.game_size[0] or down_right[1] >= self.game_size[1]:
            parsedInput[7][2] = distance
        
        # add the direction of movement
        directions = np.zeros(4)
        if inputData.direction == 0:
            directions[0] = 1
        elif inputData.direction == 1:
            directions[1] = 1
        elif inputData.direction == 2:
            directions[2] = 1
        elif inputData.direction == 3:
            directions[3] = 1
        
        # merge the vision with the direction of movement
        parsedInput = np.append(parsedInput, directions)

        return parsedInput.flatten()    

    # See? I can make a short function too
    def get_next_move(self, inputData):
        inputData = self.parse_input(inputData)
        inputWithBias = np.append(inputData, BIAS)
        hidden_layer = self.ReLU(np.dot(inputWithBias, self.W1))
        hidden_layer_with_bias = np.append(hidden_layer, BIAS)
        hidden_layer2 = self.ReLU(np.dot(hidden_layer_with_bias, self.W2))
        hidden_layer2_with_bias = np.append(hidden_layer2, BIAS)
        output = self.sigmoid(np.dot(hidden_layer2_with_bias, self.W3))
        return np.argmax(output)

    # Also this boy is short.
    # Btw I heard in one video that ReLU is better than sigmoid because it is more like a biological neuron.
    # Cool, right?
    def ReLU(self, x):
        return np.maximum(0, x)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    # Tried to make output based on the probability
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
    
    # This should probably be in the Evolution class
    def mutate(self, mutation_rate):
        # each weight has a chance to mutate
        for I in range(len(self.W1)):
            for II in range(len(self.W1[I])):
                if self.generator.random() < mutation_rate:
                    self.W1[I][II] += self.generator.normal(0, 1)
        
        for I in range(len(self.W2)):
            for II in range(len(self.W2[I])):
                if self.generator.random() < mutation_rate:
                    self.W2[I][II] += self.generator.normal(0, 1)

        for I in range(len(self.W3)):
            for II in range(len(self.W3[I])):
                if self.generator.random() < mutation_rate:
                    self.W3[I][II] += self.generator.normal(0, 1)
        return self
    

    def calculate_fitness(self, points, steps):
        self.fitness = steps + (2**points + (points**2.1) * 500) - ((points**1.2) * ((0.25 * steps)**1.3))


    def get_fitness(self, score, steps):
        return steps + (2**score + (score**2.1) * 500) - ((score**1.2) * ((0.25 * steps)**1.3))


    def clone(self):
        # deep copy of the agent
        clone = Agent(self.name, self.game_size)
        clone.W1 = np.copy(self.W1)
        clone.W2 = np.copy(self.W2)
        clone.W3 = np.copy(self.W3)
        return clone


    def save_brain(self, path):
        np.save(f"{path}-w1", self.W1)
        np.save(f"{path}-w2", self.W2)
        np.save(f"{path}-w3", self.W3)
    
    
    def load_brain(self, path):
        self.W1 = np.load(f"{path}-w1.npy")
        self.W2 = np.load(f"{path}-w2.npy")
        self.W3 = np.load(f"{path}-w3.npy")
    
    