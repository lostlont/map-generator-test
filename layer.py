import math
import opensimplex
from tools import clamp

class Layer:
	def __init__(self, width, height, scale = 1, octaves = 1):
		self.width = width
		self.height = height
		self.scale = scale
		self.octaves = octaves
		self.data = [0] * self.width * self.height

	def generate(self):
		total_weight = 2.0 - pow(0.5, self.octaves - 1)
		for noise_index in range(self.octaves):
			opensimplex.random_seed()
			scale = pow(2.0, noise_index)
			amplitude = 1.0 / scale
			for y in range(self.height):
				for x in range(self.width):
					nx = x / 16 / self.scale * scale
					ny = y / 16 / self.scale * scale
					old_value = self.get(x, y)
					next_value = self._generate_value(nx, ny) * amplitude / total_weight
					new_value = old_value + next_value
					self.set(x, y, new_value)

	def _generate_value(self, x, y):
		noise_value = opensimplex.noise2(x, y)
		normalized_value = noise_value / math.sqrt(0.5)
		return clamp(normalized_value * 0.5 + 0.5)

	def get(self, x, y):
		index = self.index(x, y)
		return self.data[index]

	def set(self, x, y, cell):
		index = self.index(x, y)
		self.data[index] = cell

	def is_valid_at(self, x, y):
		return (0 <= x) and (x < self.width) and (0 <= y) and (y < self.height)

	def index(self, x, y):
		if self.is_valid_at(x, y):
			return y * self.width + x
		else:
			raise IndexError
