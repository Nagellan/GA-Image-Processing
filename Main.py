from PIL import Image, ImageDraw
from random import randint, getrandbits
from numpy import subtract, array
import copy


IMG = Image.open("img/smoke-dog.jpg")
IMG_SIZE = IMG.size
POP_SIZE = 10
SURVIVE_COEF = 0.3
NUM_ITERATIONS = 50


class Population:
    individuals = []
    num_survived = POP_SIZE

    def create(self):
        for i in range(POP_SIZE):
            individ = Individual()
            individ.draw_figure()
            self.individuals.append(individ)


class Individual:
    fitness = -1

    def __init__(self):
        color = "black" if bool(getrandbits(1)) else "white"
        self.chromosome = Image.new('RGB', IMG_SIZE, color = color)

    def draw_figure(self):
        def pick_coords():
            coords = []

            x1 = randint(0, round(IMG_SIZE[0]*0.7))
            y1 = randint(0, round(IMG_SIZE[1]*0.7))
            coords.append(x1)
            coords.append(y1)
            coords.append(randint(x1 + round(IMG_SIZE[0]*0.2), IMG_SIZE[0]))
            coords.append(randint(y1 + round(IMG_SIZE[1]*0.2), IMG_SIZE[1]))

            return coords

        def pick_color():
            return (randint(0, 255), randint(0, 255), randint(0, 255))

        draw = ImageDraw.Draw(self.chromosome)
        coords = pick_coords()
        color = pick_color()

        self.genes = ("rectangle", coords, color)

        draw.rectangle(coords, fill=color)

    def clone(self):
        new_instance = Individual()
        new_instance.fitness = self.fitness
        new_instance.chromosome = self.chromosome.copy()
        return new_instance


class Fitness:
    def compute(self, population):
        for individ in population.individuals:
            individ.fitness = self.fitness_function(individ, IMG)
    
    def fitness_function(self, individ, img):
        fitness = 0
        img_grid = array(img)
        fig_coords = individ.genes[1]
        fig_color = individ.genes[2]

        for x in range(fig_coords[0], fig_coords[2]):
            for y in range(fig_coords[1], fig_coords[3]):
                fitness += sum(abs(subtract(img_grid[y, x], fig_color)))

        return fitness


class Selection:
    def start(self, population, coef):
        population.individuals.sort(key=lambda x: x.fitness)
        num_survived = round(POP_SIZE*coef)
        if num_survived == 0:
            num_survived = 1
        del population.individuals[num_survived:]
        population.num_survived = num_survived
        


class Crossover:
    def start(self, population):
        individuals = population.individuals

        for i in range(population.num_survived):
            for j in range(i + 1, population.num_survived):
                ind_1 = individuals[i]
                ind_2 = individuals[j]
                new_data = ind_2.chromosome.crop(ind_2.genes[1])
                new_ind = ind_1.clone()
                new_ind.chromosome.paste(new_data, (ind_2.genes[1]))
                individuals.append(new_ind)

        new_pop_size = len(individuals)
        for i in range(new_pop_size, POP_SIZE):
            new_ind = individuals[randint(0, new_pop_size - 1)].clone()
            # new_ind.chromosome = new_ind.chromosome.rotate(90*randint(1, 4), expand=False)
            individuals.append(new_ind)


def start():
    population = Population()
    population.create()

    fitness = Fitness()
    fitness.compute(population)

    selection = Selection()
    selection.start(population, SURVIVE_COEF)

    crossover = Crossover()
    crossover.start(population)


start()
