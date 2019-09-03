from generators import Generator

class Amplifier(Generator):
	"""A class to represent an amplifier"""

	def __init__(self, level=1.0, input=None, mod=None):
		self.level = level		#loudness level
		self.input = input		#amplified input
		self.mod = mod			#modulator

	def set_input(self, input):
		"""Adds an input to the amplifier"""
		self.input = input

	def set_mod(self, mod):
		"""Adds a modulator to the amplifier"""
		self.mod = mod

	def output(self, t, ignore_mod=False, **kwargs):
		"""Returns the value of the output signal in time t"""

		if ignore_mod or self.mod is None:
			mod_out = 1.0
		else:
			mod_out = self.mod.output(t, **kwargs)

		return mod_out*self.level*self.input.output(
			t, ignore_mod=ignore_mod, **kwargs
		)

	def draw(self, ax, time=1.0, **kwargs):
		"""
		Draws the shape of the output signal along with its 
		input
		
		The shape will be drawn for 'cycles' cycles of the input
		"""

		#draw the amplifiers output
		Generator.draw(self, ax, time, **kwargs)
		
		try:
			kwargs['alpha'] *= 0.5
		except KeyError:
			kwargs['alpha'] = 0.5
		
		#draw the amplifiers input
		self.input.draw(ax, time, **kwargs)


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