import numpy as np
import sounddevice as sd

import constants as const

class Generator():
	"""A class to represent a sound generator of any kind"""

	def output(self, t):
		"""Returns the value of generators signal in time t"""
		if type(t) == np.ndarray:
			return np.full(t.shape, 0.0)
		else:
			return 0.0

	def play(self, time=1.0, blocking=False):
		"""Plays the generated sound for given time (in seconds)"""
		ts = np.linspace(0, time, time*const.fs)
		sd.play(self.output(ts), const.fs, blocking=blocking)

	def draw(self, ax, time=1.0, density=100, alpha=1.0, scale=1.0):
		"""Draws the output signal"""
		ts = np.linspace(0, time, density)
		ys = scale*self.output(ts)
		ax.plot(ts, ys, alpha=alpha)

class Const(Generator):
	"""A class to represent a constant signal generator"""

	def __init__(self, value=0.0):
		self.value = np.float64(value)

	def output(self, t):
		"""Returns the value of generators signal in time t"""
		if type(t) == np.ndarray:
			return np.full(t.shape, self.value)
		else:
			return self.value

class Ramp(Generator):
	"""A class to represent a"""

	def __init__(self, slope=1.0, start=0.0):
		self.slope = np.float64(slope)
		self.start = np.float64(start)

	def output(self, t):
		"""Returns the value of generators signal in time t"""
		return self.start + self.slope*t

class Gate(Generator):
	"""A class to represent a gate generator"""

	def __init__(self, ts=[0.0, 1.0]):

		if len(ts) % 2 == 0:
			self.presses = np.array(ts[::2])
			self.releases = np.array(ts[1::2])
		else:
			self.presses = np.array(ts[::2])
			self.releases = np.zeros(self.presses.shape)
			self.releases[:-1] = np.array(ts[1::2])
			self.releases[-1] = const.inf

	def output(self, t):
		return np.sum(
			np.float64(np.logical_and(
				self.presses[i] <= t, t < self.releases[i]
			)) for i in range(len(self.presses))
		)


if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	gen = Gate([1,2,3])
	gen.draw(plt, 5)
	gen.play()
	plt.show()