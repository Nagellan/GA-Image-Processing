from PIL import Image, ImageDraw
from random import randint, getrandbits
from numpy import subtract, array
from math import sin, cos, pi
import itertools


IMG = Image.open("img/smoke-dog.jpg")
IMG_SIZE = IMG.size
POP_SIZE = 800
SURVIVE_COEF = 0.5
NUM_ITERATIONS = 3


class Population:
    individuals = []
    num_survived = POP_SIZE

    def create(self):
        for i in range(POP_SIZE):
            individ = Individual()
            individ.draw_rectangle()
            self.individuals.append(individ)


class Individual:
    fitness = -1

    def __init__(self):
        color = "black" if bool(getrandbits(1)) else "white"
        self.chromosome = Image.new('RGB', IMG_SIZE, color = color)
        self.draw = ImageDraw.Draw(self.chromosome)

    def draw_rectangle(self):
        def pick_coords():
            x1 = randint(0, round(IMG_SIZE[0]*0.7))
            y1 = randint(0, round(IMG_SIZE[1]*0.7))

            coords = [
                x1,
                y1,
                randint(x1 + round(IMG_SIZE[0]*0.2), IMG_SIZE[0]),
                randint(y1 + round(IMG_SIZE[1]*0.2), IMG_SIZE[1])
            ]

            return coords
        
        coords = pick_coords()
        color = self.pick_color()
        self.genes = (4, coords, color)
        self.draw.rectangle(coords, fill=color)

    def draw_triangle(self):
        def rotate(x, y, origin, angle):
            rads = (-angle/360)*pi
            x0, y0 = origin[0], origin[1]
            x1 = round((x-x0)*cos(rads) - (y-y0)*sin(rads) + x0)
            y1 = round((x-x0)*sin(rads) + (y-y0)*cos(rads) + y0)

            return x1, y1

        def pick_coords():
            edge_len = randint(IMG_SIZE[0]//25, IMG_SIZE[0]//2)
            x1 = randint(edge_len//2, IMG_SIZE[0] - edge_len)
            y1 = randint(edge_len//2, IMG_SIZE[1] - edge_len)
            height = round(3**(1/2)*(edge_len//2))
            origin = (x1 + edge_len//2, y1 + height//2)

            angle = randint(0, 360)

            coords = [
                rotate(x1, y1, origin, angle),
                rotate(x1 + edge_len, y1, origin, angle),
                rotate(x1 + edge_len//2, y1 + height, origin, angle)
            ]

            return coords

        coords = pick_coords()
        color = self.pick_color()
        self.draw.polygon(coords, fill=color)

    def draw_circle(self):
        def pick_coords():
            edge_len = randint(IMG_SIZE[0]//30, IMG_SIZE[0]//3)
            x1 = randint(0, IMG_SIZE[0] - edge_len)
            y1 = randint(0, IMG_SIZE[1] - edge_len)

            coords = [
                x1,
                y1,
                x1 + edge_len,
                y1 + edge_len
            ]

            return coords
        
        coords = pick_coords()
        color = self.pick_color()
        self.draw.ellipse(coords, fill=color)

    def pick_color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def clone(self):
        new_instance = Individual()
        new_instance.fitness = self.fitness
        new_instance.chromosome = self.chromosome.copy()
        new_instance.draw = ImageDraw.Draw(new_instance.chromosome)
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
        def get_comb(n, m):
            return list(itertools.combinations(range(m), n))

        individuals = population.individuals
        num_surv = population.num_survived
        num_needed = POP_SIZE - num_surv
        comb_list = get_comb(2, num_surv)[:num_needed]  # get all possible combinations of individuals crossover
        
        for (i, j) in comb_list:
            ind_1 = individuals[i]
            ind_2 = individuals[j]
            new_data = ind_2.chromosome.crop(ind_2.genes[1])
            new_ind = ind_1.clone()
            new_ind.chromosome.paste(new_data, (ind_2.genes[1]))
            individuals.append(new_ind)

        if (len(comb_list) < num_needed):   # if there're not enough offsrping, randomly clone the existing ones
            new_pop_size = len(individuals)
            for i in range(new_pop_size, POP_SIZE):
                new_ind = individuals[randint(0, new_pop_size - 1)].clone()
                individuals.append(new_ind)


class Mutation:
    def start(self, population):
        for individ in population.individuals:
            individ.draw_rectangle()    # draw rectangle
            if randint(0, 100) < 40:    # draw trangle with 20% probability
                individ.draw_triangle()
            if randint(0, 100) < 15:    # draw circle with 10% probability
                individ.draw_circle()


def start():
    population = Population()
    population.create()

    for i in range(NUM_ITERATIONS):
        fitness = Fitness()
        fitness.compute(population)

        selection = Selection()
        selection.start(population, SURVIVE_COEF)

        crossover = Crossover()
        crossover.start(population)

        mutation = Mutation()
        mutation.start(population)

        print("ITERATION " + str(i) + " COMPLETED!")
    
    fitness.compute(population)
    selection.start(population, SURVIVE_COEF)

    population.individuals[0].chromosome.save("img/art.jpg")


start()
