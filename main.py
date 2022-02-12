from quasisampler import Quasisampler, Point2D
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import sys


class ImageQuasisampler(Quasisampler):
    def __init__(self, filename: str, mag: float = 1.) -> None:
        super().__init__(0., 0.)

        self.data: List[int] = []

        # Load the grayscale image
        if not self.load_pgm(filename, mag):
            self.data = []
            self.width = self.height = 0.

    # Simple PGM parser (Low fault tolerance)
    def load_pgm(self, filename: str, mag: float = 1.) -> bool:
        if filename == '':
            raise Exception('No filename given')
        print(f'Reading PGM file {filename}')

        with open(filename, 'r') as fp:
            line = fp.readline().rstrip('\n')

            if line != 'P2':
                raise Exception('PGM file not recognized (P2 type only)')

            line = fp.readline().rstrip('\n')
            while line[0] == '#':
                line = fp.readline().rstrip('\n')

            [w, h] = line.rstrip('\n').split(' ')
            w, h = int(w), int(h)
            print(f'Got PGM file of dimensions ({w}, {h})')

            # NB: unused.
            maxval = fp.readline()

            self.data: List[int] = []
            for line in fp.read().splitlines():
                for word in line.split(' '):
                    if word != '':
                        self.data.append(int(word))

            if len(self.data) != (w*h):
                raise Exception('Incorrect number of data points (!= w*h)')

        if mag != 1.:
            self.data = [int(d * mag) for d in self.data]

        self.width = w
        self.height = h
        return True

    def get_importance_at(self, pt: Point2D) -> int:
        # Nearest pixel sampling.
        return self.data[self.width * (int(self.height - pt[1])) + int(pt[0])]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception(
            f'Usage: {sys.argv[0]} image.pgm [magnitude_factor = 200]')

    mag_factor = 200.
    if len(sys.argv) > 2:
        mag_factor = float(sys.argv[2])

    # Initialize sampler.
    print('Initializing sampler...')
    test = ImageQuasisampler(sys.argv[1], mag_factor)

    # Generate points.
    print('Getting sampling points...')
    points = test.get_sampling_points()

    # Plot points.
    # print("Printing points...")
    # for point in points:
    #     print(f'({point[0]}, {point[1]})')

    print('Plotting points...')
    xy = np.array(points)   # N x 2
    plt.scatter(xy[:, 0], xy[:, 1], s=1)
    plt.savefig('out.png')
