from biome import Biome
from color import Color
from layer import Layer
from tools import clamp

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
