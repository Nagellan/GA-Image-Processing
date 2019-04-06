from PIL import Image, ImageDraw
from random import randint, getrandbits
from numpy import subtract


IMG = Image.open("img/smoke-dog.jpg")
POP_SIZE = 1
IMG_SIZE = IMG.size
NUM_ITERATIONS = 50


class Population:
    individuals = []

    def create(self):
        for i in range(POP_SIZE):
            individ = Individual()
            individ.draw_figure()
            self.individuals.append(individ)

    def compute_fitness(self, fitness_func):
        for individ in self.individuals:
            individ.fitness = fitness_func(individ.chromosome, IMG)


class Individual:
    fitness = -1

    def __init__(self):
        color = "black" if bool(getrandbits(1)) else "white"
        self.chromosome = Image.new('RGB', IMG_SIZE, color = color)

    def draw_figure(self):
        def pick_coords():
            coords = []

            coords.append(randint(0, self.chromosome.size[0]))
            coords.append(randint(0, self.chromosome.size[1]))
            coords.append(randint(0, self.chromosome.size[0]))
            coords.append(randint(0, self.chromosome.size[1]))

            return coords

        def pick_color():
            return (randint(0, 255), randint(0, 255), randint(0, 255))

        draw = ImageDraw.Draw(self.chromosome)
        coords = pick_coords()
        color = pick_color()

        draw.rectangle(coords, fill=color)


def fitness_function(individ_chr, img):
    fitness = 0
    ind_grid = individ_chr.getdata()
    img_grid = img.getdata()

    for x in range(IMG_SIZE[0] * IMG_SIZE[1]):
        fitness += sum(abs(subtract(img_grid[x], ind_grid[x])))
    
    print(fitness)

    return fitness


def start():
    population = Population()
    population.create()

    population.compute_fitness(fitness_function)

start()
