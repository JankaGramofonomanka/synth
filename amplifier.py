from generators import Generator

class Amplifier(Generator):
	"""A class to represent an amplifier"""

	def __init__(self, level=1.0, input=None, mod=None):
		self.level = level
		self.input = input
		self.mod = mod

	def set_input(self, input):
		"""Adds an input to the amplifier"""
		self.input = input

	def set_mod(self, mod):
		"""Adds a modulator to the amplifier"""
		self.mod = mod

	def output(self, t):
		"""Returns the value of the output signal in time t"""
		if self.mod is None:
			mod_out = 1.0
		else:
			mod_out = self.mod.output(t)

		return mod_out*self.level*self.input.output(t)

	def draw(self, ax, time=1.0, density=100, alpha=1.0, scale=1.0):
		"""
		Draws the shape of the output signal along with its 
		input
		
		The shape will be drawn for 'cycles' cycles of the input
		"""

		Generator.draw(self, ax, time, density, alpha, scale)
		self.input.draw(ax, time, density, 0.5*alpha, scale)


if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	from mixer import Mixer
	from oscillators import SineOscillator, SquareOscillator

	osc = SineOscillator(440.0)
	lfo = SineOscillator(0.5)

	amp = Amplifier(2.0, osc, lfo)
	amp.play(2)
	amp.draw(plt, 4.0 / 440.0)

	plt.show()