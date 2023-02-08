import math
import numpy as np
import matplotlib.pyplot as plt


class MapGenerator:

    def __init__(self, filename, distance):
        self.filename = filename
        self.distance = distance
        self.points = self.read_points(filename)
        self.first_edge_track = []
        self.second_edge_track = []

    def read_points(self, filename):
        with open(filename, 'rt') as f:
            points = []
            for line in f:
                x, y = line.split(',')
                point = (float(x), float(y))
                points.append(point)
            return points

    def points_to_vector(self, p1, p2):
        return (p2[0] - p1[0], p2[1] - p1[1])

    def scale_vector_to_size(self, vector, size):
        norm = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        if norm:
            return (vector[0] / norm * size, vector[1] / norm * size)
        return (0, 0)

    def normalize_vector(self, vector):
        return self.scale_vector_to_size(vector, 1)

    def add_vectors(self, v1, v2):
        return (v1[0] + v2[0], v1[1] + v2[1])

    def rotate_vector(self, vector, angle):
        return (vector[0] * math.cos(angle) - vector[1] * math.sin(angle),
                vector[0] * math.sin(angle) + vector[1] * math.cos(angle))

    def get_border_points(self, p1, p2, p3):
        v1 = self.points_to_vector(p1, p2)
        v2 = self.points_to_vector(p2, p3)
        v1 = self.normalize_vector(v1)
        v2 = self.normalize_vector(v2)
        v3 = self.add_vectors(v1, v2)

        extra_distance = self.distance * (1 - np.dot(v1, v2))/2

        v3 = self.scale_vector_to_size(v3, self.distance+extra_distance)

        top = self.rotate_vector(v3, math.pi / 2)
        bottom = self.rotate_vector(v3, -math.pi / 2)

        self.first_edge_track.append(self.add_vectors(p2, top))
        self.second_edge_track.append(self.add_vectors(p2, bottom))

    def generate_track(self):
        for i in range(len(self.points) - 2):
            self.get_border_points(self.points[i], self.points[i + 1],
                                   self.points[i + 2])

    def get_tracks(self):
        return self. points, self.first_edge_track, self.second_edge_track

    def display_map(self):
        self.generate_track()
        x = [p[0] for p in self.points]
        y = [p[1] for p in self.points]
        plt.plot(x, y, 'k-')
        x = [p[0] for p in self.first_edge_track]
        y = [p[1] for p in self.first_edge_track]
        plt.plot(x, y, 'k-')
        x = [p[0] for p in self.second_edge_track]
        y = [p[1] for p in self.second_edge_track]
        plt.plot(x, y, 'k-')
        plt.show()


if __name__ == '__main__':
    map_generator = MapGenerator('track.txt', 4)
    map_generator.display_map()
