from generator import Generator

class Amplifier(Generator):
	"""A class to represent an amplifier"""

	def __init__(self, level=1.0, input=None):
		self.level = level
		self.input = input

	def output(self, t):
		"""Returns the value of the output signal in time t"""
		return self.level*self.input.output(t)

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

	mixer = Mixer()

	mixer.add_input(SineOscillator(440.0, 0.5))
	mixer.add_input(SineOscillator(660.0, 0.5))

	amp = Amplifier(2.0, mixer)
	amp.play()
	amp.draw(plt, 1.0 / 330.0)

	plt.show()