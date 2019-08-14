import numpy as np
import sounddevice as sd

class Generator():
	"""A class to represent a sound generator of any kind"""

	fs = 44100		#sample rate

	def output(self, t):
		"""Returns the value of generators signal in time t"""
		if type(t) == np.ndarray:
			return np.full(t.shape, 0.0)
		else:
			return 0.0

	def play(self, time=1.0, blocking=False):
		"""Plays the generated sound for given time (in seconds)"""
		ts = np.linspace(0, time, time*self.fs)
		sd.play(self.output(ts), self.fs, blocking=blocking)

	def draw(self, ax, time=1.0, density=100, alpha=1.0, scale=1.0):
		"""Draws the output signal"""
		ts = np.linspace(0, time, density)
		ys = scale*self.output(ts)
		ax.plot(ts, ys, alpha=alpha)

if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	gen = Generator()
	gen.draw(plt)
	gen.play()
	plt.show()