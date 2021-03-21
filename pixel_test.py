import board
import neopixel
#pixels = neopixel.NeoPixel(board.D5, 30)    # Feather wiring!
pixels = neopixel.NeoPixel(board.D18, 50, brightness = 0.5) # Raspberry Pi wiring!

#pixels.fill((255, 64, 0)) # burnt orange - ISS in sunlight

#pixels.fill((5, 0, 25)) # twilight - ISS in dark

pixels.fill((255, 255, 255)) # Bright White - ISS above my horizon