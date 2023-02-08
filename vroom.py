import pygame
import math
import random
import mapGenerator as mg

# initialize the pygame library
pygame.init()

# define screen size
screen_width = 1440
screen_height = 880
screen = pygame.display.set_mode((screen_width, screen_height))

# define car class


class Car:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.hitbox = image.get_rect()
        self.speed = 0
        self.angle = 0

    def drive(self, speed, angle):
        self.speed = speed
        self.angle = angle

        # convert angle from degrees to radians
        angle = math.radians(angle)

        # update the x and y position based on angle and speed
        self.x += math.sin(angle) * speed
        self.y -= math.cos(angle) * speed

    def draw(self, screen):
        car_image = self.image
        car_image = pygame.transform.rotate(car_image, -self.angle)

        car_rect = car_image.get_rect()
        car_rect.center = (self.x, self.y)
        screen.blit(car_image, car_rect)


class Edge:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (self.x1, self.y1),
                         (self.x2, self.y2), 4)


class Game:
    def __init__(self) -> None:
        self.track = []

    def create_edges(self, track_points, complete_loop=True):
        edges = []
        for i in range(len(track_points)-1+complete_loop):
            x1, y1 = track_points[i]
            x2, y2 = track_points[(i + 1) % len(track_points)
                                  ] if complete_loop else track_points[i+1]
            edges.append(Edge(x1, y1, x2, y2))
        return edges

    def read_points(self, filename):
        track_points = []
        with open(filename, "r") as f:
            for line in f:
                track_points.append(tuple(map(float, line.split(","))))
        return track_points

    def find_track_scale(self, edges):
        # find the minimum and maximum x and y values in the lines
        min_x, min_y, max_x, max_y = float('inf'), float(
            'inf'), float('-inf'), float('-inf')
        for edge in edges:
            x1, y1 = edge.x1, edge.y1
            x2, y2 = edge.x2, edge.y2
            min_x = min(min_x, x1, x2)
            min_y = min(min_y, y1, y2)
            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)

        # find the scale factor to fit the track into the screen
        scale_x = screen_width / (max_x - min_x)
        scale_y = screen_height / (max_y - min_y)
        scale = min(scale_x, scale_y)

        # find the center of the track
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2

        return scale, center_x, center_y

    def draw_track(self, edges, scale, center_x, center_y):
        color = (0, 0, 0)

        # set the line width
        line_width = 4

        # draw the scaled lines
        for edge in edges:
            x1, y1 = edge.x1, edge.y1
            x2, y2 = edge.x2, edge.y2
            x1 = (x1 - center_x) * scale + screen_width // 2
            y1 = (y1 - center_y) * scale + screen_height // 2
            x2 = (x2 - center_x) * scale + screen_width // 2
            y2 = (y2 - center_y) * scale + screen_height // 2
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), line_width)


if __name__ == "__main__":
    # initialize the car and edges
    car_image = pygame.image.load("images/car.jpeg")
    # scale down the image
    car_image = pygame.transform.scale(
        car_image, (car_image.get_width() // 7, car_image.get_height() // 7))
    car = Car(200, 340, car_image)
    # edges that form a looped course

    # read points from track.txt

    game = Game()
    generator = mg.MapGenerator('track.txt', 4)
    generator.generate_track()

    track_points, top_edge, bottom_edge = generator.get_tracks()

    top_edge = game.create_edges(top_edge)
    bottom_edge = game.create_edges(bottom_edge)
    scale, center_x, center_y = game.find_track_scale(top_edge)

    # run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # update the car based on user inputs
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            car.speed = 1
        elif keys[pygame.K_DOWN]:
            car.speed = -0.5
        else:
            car.speed = 0

        if keys[pygame.K_LEFT]:
            car.angle -= 0.8
        elif keys[pygame.K_RIGHT]:
            car.angle += 0.8

        if keys[pygame.K_h]:
            car.show_hitbox = not car.show_hitbox

        car.drive(car.speed, car.angle)

        # clear the screen
        screen.fill((255, 255, 255))

        # draw the track
        game.draw_track(top_edge, scale, center_x, center_y)
        game.draw_track(bottom_edge, scale, center_x, center_y)
        # draw the car and edges
        car.draw(screen)

        # update the display
        pygame.display.flip()

    # quit the pygame library
    pygame.quit()
