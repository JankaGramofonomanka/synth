import numpy as np

from generators import Generator

class Mixer(Generator):
	"""A class to represent a mixer"""

	def __init__(self):
		self.inputs = []	#list of inputs
		self.levels = []	#list of loudness levels

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

	def output(self, t, **kwargs):
		"""Returns the sum of the values of all inputs at time t"""
		if self.inputs == []:
			if type(t) == np.ndarray:
				return np.full(t.shape, 0.0)
			else:
				return 0.0
		else:
			return np.sum(
				self.levels[i]*self.inputs[i].output(t, **kwargs) 
				for i in range(len(self.inputs))
			)

	def draw(self, ax, time=1.0, **kwargs):
		"""
		Draws the shape of the output signal along with its 
		inputs
		"""
		#draw the output signal
		Generator.draw(self, ax, time, **kwargs)

		#draw inputs' output signals
		for i in range(len(self.inputs)):
			try:
				kwargs['alpha'] *= 0.5
			except KeyError:
				kwargs['alpha'] = 0.5

			try:
				kwargs['scale'] *= self.levels[i]
			except KeyError:
				kwargs['scale'] = self.levels[i]
			
			self.inputs[i].draw(ax, time, **kwargs)

if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	from oscillators import SineOscillator, SquareOscillator, SawOscillator

	mixer = Mixer()

	mixer.add_input(SawOscillator(440.0))
	mixer.add_input(SawOscillator(1.5*440.0))

	mixer.set_level(0, 0.5)
	mixer.set_level(1, 0.5)

	mixer.draw(plt, 4.0 / 440.0, density=400)
	mixer.play()
	plt.show()