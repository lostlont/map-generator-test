#!/bin/env python
import png
from map import Map

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

def save_image(pixels, filename):
	png_image = png.from_array(pixels, 'RGB')
	png_image.save(filename)

if __name__ == '__main__':
	run()
