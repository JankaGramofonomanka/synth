import numpy as np
import sounddevice as sd

from generators import Generator

class Oscillator(Generator):
	"""A class to represent a basic oscillator"""

	freq = 440.0 	#generators frequency

	def output(self, t):
		"""Returns the value of generators signal in time t"""
		return np.sin(self.freq*2*np.pi*t)

	def draw(self, ax, time=None, density=100, alpha=1.0, scale=1.0, cycles=1):
		"""Draws the signals wave shape"""
		if time is None:
			time = cycles / float(self.freq)
			density = density*cycles

		Generator.draw(self, ax, time, density, alpha, scale)

class SineOscillator(Oscillator):
	"""A class to represent a sine wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0):

		#initialize essential parameters
		self.freq = freq
		self.amp = amp
		self.phase = phase

	def output(self, t):
		"""Returns the value of oscillators signal in time t"""
		return self.amp*np.sin(self.freq*2*np.pi*t + self.phase)

class SquareOscillator(Oscillator):
	"""A class to represent a square wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0):
		
		#initialize essential parameters
		self.freq = freq
		self.amp = amp
		self.phase = phase

	def output(self, t):
		"""Returns the value of oscillators signal in time t"""
		return self.amp*np.sign(np.sin(self.freq*2*np.pi*t + self.phase))

if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	osc = SineOscillator(440.0, 0.5)
	
	osc.draw(plt, cycles=5, scale=20, density=5)
	osc.play()
	plt.show()