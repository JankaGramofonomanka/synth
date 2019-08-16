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

	def __init__(self, freq=440.0, amp=1.0, phase=0.0, pw=0.5):
		
		#initialize essential parameters
		self.freq = freq
		self.amp = amp
		self.phase = phase
		self.pw = pw

	def output(self, t):
		"""Returns the value of oscillators signal in time t"""
		current_phase = (self.freq*t + (self.phase / (2*np.pi))) % 1.0

		return self.amp*(2*np.float64(current_phase < self.pw) - 1)

class SawOscillator(Oscillator):
	"""A class to represent a saw wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0):
		
		#initialize essential parameters
		self.freq = freq
		self.amp = amp
		self.phase = phase

	def output(self, t):
		"""Returns the value of oscillators signal in time t"""
		return self.amp*(
			-2*((self.freq*t + (self.phase / (2*np.pi))) % 1.0) + 1
		)

class RampOscillator(SawOscillator):
	"""A class to represent a ramp wave oscillator"""

	def output(self, t):
		"""Returns the value of oscillators signal in time t"""
		return -SawOscillator.output(self, t)

class TriangleOscillator(Oscillator):
	"""A class to represent a saw wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0, pw=0.5):
		
		#initialize essential parameters
		self.freq = freq
		self.amp = amp
		self.phase = phase
		self.pw = pw

	def output(self, t):
		"""Returns the value of oscillators signal in time t"""
		current_phase = (self.freq*t + (self.phase / (2*np.pi))) % 1.0
		square = np.float64(current_phase < self.pw)

		return self.amp*(
			2*(
				current_phase*square / self.pw + 
				(1 - current_phase)*(1 - square) / (1 - self.pw)
			) - 1
		)


if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	osc = SquareOscillator(440.0, pw=0.25)
	
	osc.draw(plt, cycles=2)
	osc.play()
	plt.show() 