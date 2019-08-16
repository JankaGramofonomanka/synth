import numpy as np

from generators import Generator

class Mixer(Generator):
	"""A class to represent a mixer"""

	inputs = []
	levels = []

	def add_input(self, input, level=1.0):
		"""Adds an input to the mixer"""

		self.inputs.append(input)
		self.levels.append(level)

	def set_level(self, i, level):
		"""Changes the level corresponding to the i-th input"""
		self.levels[i] = level

	def increase_level(self, i, level=0.01):
		"""Increases the level corresponding to the i-th input"""
		self.levels[i] += level

	def decrease_level(self, i, level=0.01):
		"""Decreases the level corresponding to the i-th input"""
		self.increase_level(i, -level)

	def output(self, t):
		"""Returns the sum of the values of all inputs at time t"""
		if self.inputs == []:
			return 0.0
		else:
			return np.sum(
				self.levels[i]*self.inputs[i].output(t) 
				for i in range(len(self.inputs))
			)

	def draw(self, ax, time=1.0, density=100, alpha=1.0, scale=1.0):
		"""
		Draws the shape of the output signal along with its 
		inputs
		"""
		#draw the output signal
		Generator.draw(self, ax, time, density, alpha)

		#draw inputs' output signals
		for i in range(len(self.inputs)):
			self.inputs[i].draw(
				ax, time, density, 0.5*alpha, self.levels[i]*scale
			)

if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	from oscillators import SineOscillator, SquareOscillator

	mixer = Mixer()

	n = 11
	for i in range(1, n):
		mixer.add_input(SineOscillator(i*440.0))

	for i in range(1, n):
		mixer.set_level(i - 1, 1.0 / i)

	mixer.draw(plt, 1.0 / 440.0, 400)
	mixer.play()
	plt.show()