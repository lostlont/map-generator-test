from enum import Enum
from color import Color
from tools import clamp

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
