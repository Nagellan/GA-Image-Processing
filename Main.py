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
            individ.draw_figure()
            self.individuals.append(individ)


class Individual:
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

        draw.rectangle(coords, fill=color)


def start():
    population = Population()
    population.create()


start()