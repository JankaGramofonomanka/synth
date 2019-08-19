import numpy as np

import constants as const

from generators import Generator, Gate

class MonoKey(Generator):
	"""
	A class to represent a part of a keybord that sends an output signal 
	represeting which key is pressed at a given time
	"""

	def __init__(self, steps=[], pitches=[]):

		if len(steps) < len(pitches):
			pitches = pitches[:len(steps)]

		self.steps = np.full((len(steps) + 2), 0.0)
		self.pitches = np.full((len(pitches) + 1), 0, dtype=np.int32)

		self.steps[0] = 0
		self.steps[1:-1] = steps
		self.steps[-1] = const.inf

		self.pitches[0] = 0.0
		self.pitches[1:] = pitches

	def output(self, t, **kwargs):
		"""Returns the value of generators signal in time t"""
		return np.sum(
			self.pitches[i]*np.int32(
				np.logical_and(self.steps[i] <= t, t < self.steps[i + 1])
			) for i in range(len(self.pitches))
		)

class MonoKeyboard():
	"""A class to represent a monophonic keyboard"""

	def __init__(self, gate=Gate([]), pitches=[], steps=None):

		self.gate = gate
		if steps is None:
			steps = gate.presses

		self.key = MonoKey(steps, pitches)

	def key_out(self, t, **kwargs):
		return self.key.output(t, **kwargs)

	def gate_out(self, t, **kwargs):
		return self.gate.output(t, **kwargs)


if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	gate = Gate([1, 2.5, 3, 3.2, 4, 4.05, 4.3, 5, 6, 7., 9])
	kbd = MonoKeyboard(gate, [4, 5, 2, -3, 0, 1, 3, -2], [1, 3, 4, 4.3, 4.7, 6, 6.5])

	kbd.gate.draw(plt, 10, density=800)
	kbd.key.draw(plt, 10, density=800)

	plt.show()