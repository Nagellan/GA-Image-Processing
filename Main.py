from PIL import Image, ImageDraw
from random import randint, getrandbits


IMG = Image.open("img/smoke-dog.jpg")
POP_SIZE = 5
IMG_SIZE = IMG.size
NUM_ITERATIONS = 50


class Population:
    individuals = []

    def create(self):
        for i in range(POP_SIZE):
            individ = Individual()
            individ.draw_polygon()
            self.individuals.append(individ)


class Individual:
    def __init__(self):
        color = "black" if bool(getrandbits(1)) else "white"
        self.chromosome = Image.new('RGB', IMG_SIZE, color = color)

    def draw_polygon(self):
        def pick_coords():
            coords = []
            for i in range(4):
                coords.append((randint(0, self.chromosome.size[0]), randint(0, self.chromosome.size[1])))
            return coords

        def pick_color():
            return (randint(0, 255), randint(0, 255), randint(0, 255))

        draw = ImageDraw.Draw(self.chromosome)
        coords = pick_coords()
        color = pick_color()

        draw.polygon(coords, fill=color)


def start():
    population = Population()
    population.create()


start()