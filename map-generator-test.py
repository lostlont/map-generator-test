#!/bin/env python
import png

def run():
	print("Test!")
	pixels = []
	for y in range(256):
		row = []
		for x in range(256):
			row.append((x*y) % 256)
			row.append((x+y) % 256)
			row.append(abs(x-y) % 256)
		pixels.append(row)
	pngImage = png.from_array(pixels, 'RGB')
	pngImage.save('out.png')

if __name__ == '__main__':
	run()
