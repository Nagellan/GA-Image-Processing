from PIL import Image, ImageDraw
from random import randint

IMG = Image.open("img/smoke-dog.jpg")
POP_SIZE = 5
IMG_SIZE = IMG.size
NUM_ITERATIONS = 50

def create_init_population(img_size, pop_size):
    population = []

    for i in range(pop_size):
        img = Image.new('RGB', img_size, color = 'black')
        draw_polygon(img)
        population.append(img)

    return population


def draw_polygon(img):
    def pick_coords():
        coords = []
        for i in range(4):
            coords.append((randint(0, img.size[0]), randint(0, img.size[1])))
        return coords

    def pick_color():
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    draw = ImageDraw.Draw(img)
    coords = pick_coords()
    color = pick_color()

    draw.polygon(coords, fill=color)


def start():
    population = create_init_population(IMG_SIZE, POP_SIZE)


start()