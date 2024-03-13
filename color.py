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
