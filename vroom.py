import pygame
import math
import random

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
                         (self.x2, self.y2), 100)


# initialize the car and edges
car_image = pygame.image.load("images/car.jpeg")
# scale down the image
car_image = pygame.transform.scale(
    car_image, (car_image.get_width() // 7, car_image.get_height() // 7))
car = Car(320, 240, car_image)
# edges that form a looped course


def car_on_edge(car, edge, width=100):
    car_x = car.x
    car_y = car.y
    x1, y1, x2, y2 = edge.x1, edge.y1, edge.x2, edge.y2
    min_x = min(x1, x2) - width/2
    max_x = max(x1, x2) + width/2
    min_y = min(y1, y2) - width/2
    max_y = max(y1, y2) + width/2

    if car_x >= min_x and car_x <= max_x and car_y >= min_y and car_y <= max_y:
        return True

    return False


def points_to_edges(points):
    edges = []
    for i in range(len(points)):
        edges.append(Edge(points[i][0], points[i][1],
                     points[i-1][0], points[i-1][1]))
    return edges


# read points from track.txt
track_points = []
with open("track.txt", "r") as f:
    for line in f:
        track_points.append(tuple(map(float, line.split(","))))

        track_points[-1] = (track_points[-1][0] + 100,
                            track_points[-1][1] + 100)

        track_points[-1] = (track_points[-1][0] ** 1.5,
                            track_points[-1][1] ** 1.5)

        track_points[-1] = (track_points[-1][0] - 300,
                            track_points[-1][1] - 250)


edges = points_to_edges(track_points)


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

    for edge in edges:
        edge.draw(screen)
    # draw the car and edges
    car.draw(screen)

    for edge in edges:
        if car_on_edge(car, edge):
            print("Car is on an edge.")
            break
    else:
        print("Car is not on an edge.")

    # update the display
    pygame.display.flip()

# quit the pygame library
pygame.quit()
