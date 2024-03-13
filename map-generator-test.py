#!/bin/env python
from enum import Enum
import math
import png
import opensimplex

def clamp(value, min_value = 0.0, max_value = 1.0):
	return min(max(value, min_value), max_value)

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

					noise_value = opensimplex.noise2(nx, ny)
					normalized_value = noise_value / math.sqrt(0.5)
					noise_value = clamp(normalized_value * 0.5 + 0.5)

					next_value = noise_value * amplitude / total_weight
					new_value = old_value + next_value
					self.set(x, y, new_value)

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

class Color:
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b

	def __mul__(self, value):
		r = self.r * value
		g = self.g * value
		b = self.b * value
		return Color(r, g, b)

class Biome(Enum):
	SNOWY_TUNDRA = 1
	SNOWY_TAIGA = 2
	PLAINS = 3
	FOREST = 4
	TAIGA = 5
	GIANT_SPRUCE_TAIGA = 6
	BIRCH_FOREST = 7
	DARK_FOREST = 8
	SAVANNA = 9
	JUNGLE = 10
	DESERT = 11
	JUNGLE_EDGE = 12

	def at(temperature, humidity):
		biome_map = [
			[Biome.SNOWY_TUNDRA, Biome.PLAINS, Biome.PLAINS, Biome.SAVANNA, Biome.DESERT],
			[Biome.SNOWY_TUNDRA, Biome.PLAINS, Biome.PLAINS, Biome.SAVANNA, Biome.DESERT],
			[Biome.SNOWY_TUNDRA, Biome.FOREST, Biome.FOREST, Biome.FOREST, Biome.DESERT],
			[Biome.SNOWY_TAIGA, Biome.TAIGA, Biome.BIRCH_FOREST, Biome.JUNGLE, Biome.JUNGLE_EDGE],
			[Biome.SNOWY_TAIGA, Biome.GIANT_SPRUCE_TAIGA, Biome.DARK_FOREST, Biome.JUNGLE, Biome.JUNGLE],
		]
		x = clamp(int(temperature * 5), 0, 4)
		y = clamp(int(humidity * 5), 0, 4)
		return biome_map[y][x]

	def color(self):
		match self:
			case Biome.SNOWY_TUNDRA: return Color(1.0, 1.0, 1.0)
			case Biome.SNOWY_TAIGA: return Color(0.192, 0.333, 0.29)
			case Biome.PLAINS: return Color(0.553, 0.702, 0.376)
			case Biome.FOREST: return Color(0.02, 0.4, 0.129)
			case Biome.TAIGA: return Color(0.043, 0.4, 0.349)
			case Biome.GIANT_SPRUCE_TAIGA: return Color(0.506, 0.557, 0.475)
			case Biome.BIRCH_FOREST: return Color(0.188, 0.455, 0.267)
			case Biome.DARK_FOREST: return Color(0.408, 0.475, 0.259)
			case Biome.SAVANNA: return Color(0.741, 0.698, 0.373)
			case Biome.JUNGLE: return Color(0.325, 0.482, 0.035)
			case Biome.DESERT: return Color(0.98, 0.58, 0.094)
			case Biome.JUNGLE_EDGE: return Color(0.384, 0.545, 0.09)

class Map:
	def __init__(self, width, height, scale = 1):
		self.width = width
		self.height = height
		self.scale = scale

	def generate(self):
		self.peaks_layer = Layer(self.width, self.height, self.scale * 4, octaves = 8)
		self.peaks_layer.generate()
		self.continentalness_layer = Layer(self.width, self.height, scale = 8 * self.scale, octaves = 3)
		self.continentalness_layer.generate()
		self.temperature_layer = Layer(self.width, self.height, scale = 32 * self.scale, octaves = 3)
		self.temperature_layer.generate()
		self.humidity_layer = Layer(self.width, self.height, scale = 16 * self.scale, octaves = 3)
		self.humidity_layer.generate()

	def render(self):
		return self._render_by(self._get_combined_color)

	def _get_combined_color(self, x, y):
		peak = self.peaks_layer.get(x, y)
		continentalness = self.continentalness_layer.get(x, y)
		temperature = self.temperature_layer.get(x, y)
		humidity = self.humidity_layer.get(x, y)

		if continentalness < 0.4:
			ridge_count = 4
			continental_ridge = int(continentalness / 0.4 * ridge_count) / ridge_count
			brightness = 0.5 + continental_ridge * 0.5
			color = Color(0.24, 0.28, 0.97)
		else:
			riverness = (temperature + humidity + peak * 0.25) % 0.4
			if (riverness < 0.01) or (0.39 <= riverness):
				color = Color(0.30, 0.34, 0.98)
				brightness = 1.0
			else:
				continental_height = (continentalness - 0.4) / 0.6
				height = continental_height * 0.6 + (peak * pow(continental_height, 0.3) * 0.4)
				brightness = 0.75 + height * 0.4
				biome = Biome.at(temperature, humidity)
				color = biome.color()

		color *= brightness
		return color

	def render_peaks(self):
		def get_peak_color(x, y):
			value = self.peaks_layer.get(x, y)
			return Color(value, value, value)
		return self._render_by(get_peak_color)

	def render_continentalness(self):
		def get_continentalness_color(x, y):
			value = self.continentalness_layer.get(x, y)
			return Color(value, value, value)
		return self._render_by(get_continentalness_color)

	def render_temperature(self):
		def get_temperature_color(x, y):
			value = self.temperature_layer.get(x, y)
			return Color(value, value, value)
		return self._render_by(get_temperature_color)

	def render_humidity(self):
		def get_humidity_color(x, y):
			value = self.humidity_layer.get(x, y)
			return Color(value, value, value)
		return self._render_by(get_humidity_color)

	def _render_by(self, function):
		pixels = []
		for y in range(self.height):
			row = []
			for x in range(self.width):
				color = function(x, y)
				row.append(int(clamp(color.r) * 255))
				row.append(int(clamp(color.g) * 255))
				row.append(int(clamp(color.b) * 255))
			pixels.append(row)
		return pixels

def save_image(pixels, filename):
	png_image = png.from_array(pixels, 'RGB')
	png_image.save(filename)

def run():
	size = 512
	scale = 0.5
	map = Map(size, size, scale)
	map.generate()
	save_image(map.render(), 'map.png')
	save_image(map.render_peaks(), 'map-peaks.png')
	save_image(map.render_continentalness(), 'map-continentalness.png')
	save_image(map.render_temperature(), 'map-temperature.png')
	save_image(map.render_humidity(), 'map-humidity.png')

if __name__ == '__main__':
	run()
