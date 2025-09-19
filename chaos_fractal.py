import numpy as np
import random
import pygame

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ChaosFractal:
    def __init__(self, verticies=3, size=600, steps=100000, batch=100, factor=0.5,
                 margin=0.95, canRepeat=True, weights=None):
        self.verticies = verticies
        self.size = size
        self.margin = margin
        self.factor = factor
        self.center = self.size // 2
        self.steps = steps
        self.batch = batch
        self.canRepeat = canRepeat
        self.weights = weights or [1] * verticies
        self.mainVerticies = self.calculateMainVerticies()
        self.previous_vertex = self.mainVerticies[0]
        self.x = random.uniform(0, self.size)
        self.y = random.uniform(0, self.size)
        self.points_generated = 0

        pygame.init()
        self.screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption(f"{verticies}-Vertex Chaos Fractal")
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))

    def calculateMainVerticies(self):
        degBetween = 2 * np.pi / self.verticies
        rotation = -np.pi / 2 - np.pi / self.verticies

        maxRadiusX = (self.size / 2) * self.margin
        maxRadiusY = (self.size / (1 + np.sin(np.pi / self.verticies))) * self.margin
        radius = min(maxRadiusX, maxRadiusY)

        result = []
        for i in range(self.verticies):
            angle = degBetween * i + rotation
            x = self.center + np.cos(angle) * radius
            y = self.center - np.sin(angle) * radius
            result.append(Point(x, y))
        return result

    def setNextPoint(self, display):
        attempt_limit = 100
        attempts = 0

        while attempts < attempt_limit:
            vertex = random.choices(self.mainVerticies, weights=self.weights, k=1)[0]
            if not self.canRepeat:
                while vertex == self.previous_vertex:
                    vertex = random.choices(self.mainVerticies, weights=self.weights, k=1)[0]
                self.previous_vertex = vertex

            self.x = self.x + self.factor * (vertex.x - self.x)
            self.y = self.y + self.factor * (vertex.y - self.y)

            xi, yi = round(self.x), round(self.y)

            if 0 <= xi < self.size and 0 <= yi < self.size:
                if display[xi, yi] != (0 << 16) + (0 << 8) + 0:
                    display[xi, yi] = (0 << 16) + (0 << 8) + 0
                    self.points_generated += 1
                    break

            attempts += 1

    def run(self):
        running = True
        generating = True
        pixels = pygame.PixelArray(self.screen)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        generating = not generating
                    elif event.key == pygame.K_ESCAPE:
                        generating = False
                        save = input("Would you like to save? ('Yes' or 'No'): ").lower()
                        if (save == "yes"):
                            filename = f"saved_fractals\chaos_fractal_{self.verticies}_vertices.png"
                            pygame.image.save(self.screen, filename)
                            print(f"Fractal saved as {filename}")
                        running == False
            if generating:
                for _ in range(self.batch):
                    self.setNextPoint(pixels)

            pygame.display.flip()
            self.clock.tick(60)

        del pixels
        pygame.quit()

def str_to_bool(s):
    return s.lower() in ["1", "true", "yes"]

def main():
    displaySize = 800
    margin = 0.95
    batchSize = 250
    numSteps = 1000000
    factor = 0.5
    canRepeat = True
    verticies = 3
    weights = None

    try:
        verticies = int(input(f"Number of vertices: ") or verticies)
        custom = input("Custom Fractal? ('Yes' or 'No'): ").lower()
        if custom == "yes":
            factor = float(input(f"Contraction factor (0-1): ") or factor)
            canRepeat = str_to_bool(input(f"Allow consecutive repeats? (True/False): ") or str(canRepeat))
            customWeights = input("Custom weights? ('Yes' or 'No'): ")
            if customWeights.lower() == "yes":
                weights_input = input("Enter vertex weights separated by commas, or type 'random': ")
                if weights_input.lower() == "random":
                    weights = [round(random.uniform(0.1, 1.0), 3) for _ in range(verticies)]
                    print(f"Randomly generated weights: {weights}")
                elif weights_input:
                    weights = [float(w) for w in weights_input.split(",")]
            else:
                weights = None
    except ValueError:
        print("Invalid input, using defaults.")
        weights = None
    print("Creating Fractal...")
    print("Press 'Space' to Pause or Resume generation")

    fractal = ChaosFractal(
        verticies=verticies,
        steps=numSteps,
        batch=batchSize,
        size=displaySize,
        margin=margin,
        factor=factor,
        canRepeat=canRepeat,
        weights=weights
    )

    fractal.run()

if __name__ == "__main__":
    main()
