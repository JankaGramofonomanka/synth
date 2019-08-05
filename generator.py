import numpy as np
import sounddevice as sd

class Generator():
	"""A class to represent a sound generator of any kind"""

	freq = 440.0 	#generators frequency
	fs = 44100		#sample rate

	def wave_y(self, t):
		"""Returns the value of generators signal in time t"""
		return np.sin(self.freq*2*np.pi*t)

	def play(self, time=1.0, blocking=False):
		"""Plays the generated sound for given time (in seconds)"""
		ts = np.linspace(0, time, time*self.fs)
		sd.play(self.wave_y(ts), self.fs, blocking=blocking)

	def draw(self, ax, cycles=1, alpha=1.0):
		"""Draws the signals wave shape"""
		ts = np.linspace(0, cycles / float(self.freq), 100*cycles)
		ys = self.wave_y(ts)
		ax.plot(ts, ys, alpha=alpha)

if __name__ == '__main__':

	#the code below is just tests
	import matplotlib.pyplot as plt

	gen = Generator()
	gen.draw(plt)
	gen.play()
	plt.show()