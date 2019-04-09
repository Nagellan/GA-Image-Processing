# AI: Assignment 2

## Task

The full task can be read [here](Assignment2.pdf).

Given several test input images of 512x512 pixels, using any programming language produce via any **evolutionary algorithm** another 512x512 image from a single test one by using your _computational artist_ (algorithm).

The outcome must be a **piece of art** and will be evaluated in the art contest by both students and experts panel (including artists and poets, some computational artists and some analog from about the globe).

#### **Everything below may be changed completely or just partialy during the development process!**

## Plan

- [x] Read about Genetic algorithm basics
- [x] Read about image recognition and processing
- [x] Choose the technology stack
- [x] Create a GitHub Repository
- [x] Implement Genetic algorithm
- [x] Include image segmentation and processing
- [ ] Integrate the project with Flask `Postponed`
- [ ] Add user interface for interacting with the program `Postponed`
- [ ] Deploy the whole project on server `Postponed`

## Architecture stack

1. **Python** for the backend
    1. **Pillow** framework for image processing
    2. **Scikit-image** module for image segmentation `Rejected`
2. **Flask** for transformation the project into the web-application `Postponed`
3. **HTML + CSS + JS** for the frontend `Postponed`
4. **Heroku** as the place for project deployment `Postponed`

## Implementation

The full report is available [here](Report.pdf).

### Initial population
On this stage, the necessary amount (specified initially) of individuals is generated.
The individual’s chromosome is the picture with the black or white background (chosen randomly) and the rectangle of some random color on it.
The rectangle’s coordinates and color are saved as the individual’s genes. Rectangles for my algorithm are the same as the brush strokes on the paintings.

### Fitness function
On this stage, comparisons with the origin image happen.
From the individual, I take genes with the information about coordinates of the last added rectangle and its color. Then I compare pixels on the origin picture lying on the appropriate area of that rectangle (lying on individual’s chromosome) with its color. I find the difference between each pixel on that area and rectangle color, and them sum it to the individual’s fitness score.

### Selection
On this stage, the whole population is sorted increasingly by the fitness score and then reduced by the survival coefficient specified initially.

### Crossover
On this stage, the population is restored by crossing the best survived individuals.
Pairwisely, all the combinations of survived individuals are crossed in following way: the area of last added rectangle is copied from one individual to another (from worse individual to the better one). If the amount of combinations is not enough to restore the population to its initial amount, it’s finally complemented by random creatures already existing.

### Mutation
On this stage, the new figures are added with some probability to each individual.
The rectangle is added with 100% probability.
The triangle is added with 40% probability.
The circle is added with 15% probability.

All these stages (except the first one) are being repeated until the specified number of iterations is done.


## Useful links

* [Introduction to evolutionary algorithms](https://towardsdatascience.com/introduction-to-evolutionary-algorithms-a8594b484ac)
* [Introduction to genetic algorithms with example on Java](https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3)
* [Mona Lisa example FAQ](https://rogerjohansson.blog/2008/12/09/genetic-programming-mona-lisa-faq/)
* [Wiki: Image segmentation](https://en.wikipedia.org/wiki/Image_segmentation)
* [Pillow Python library for image processing](https://pillow.readthedocs.io/en/stable/)
* [Scikit-image module for image segmentation in Python](https://towardsdatascience.com/image-segmentation-using-pythons-scikit-image-module-533a61ecc980)

### Articles

* [Image enhancement incorporating fuzzy fitness function in genetic algorithms](https://www.isical.ac.in/~malay/Papers/Conf/FUZZIEEE_1993.pdf)
* [A Review of Genetic Algorithm application for Image Segmentation](https://pdfs.semanticscholar.org/4d99/dffc47a0c8a6d750e54f0207976ce30a3210.pdf)
* [Image segmentation using genetic algorithm and
morphological operations](https://lib.dr.iastate.edu/cgi/viewcontent.cgi?article=1262&context=rtd)
