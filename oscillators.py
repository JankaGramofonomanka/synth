import numpy as np
import sounddevice as sd

from generator import Generator

class SineOscillator(Generator):
	"""A class to represent a sine wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0):

		#initialize essential parameters
		self.freq = freq
		self.amp = amp
		self.phase = phase

	def wave_y(self, t):
		"""Returns the value of oscillators signal in time t"""
		return self.amp*np.sin(self.freq*2*np.pi*t + self.phase)

class SquareOscillator(Generator):
	"""A class to represent a square wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0):
		
		#initialize essential parameters
		self.freq = freq
		self.amp = amp
		self.phase = phase

	def wave_y(self, t):
		"""Returns the value of oscillators signal in time t"""
		return self.amp*np.sign(np.sin(self.freq*2*np.pi*t + self.phase))

if __name__ == '__main__':

	#the code below is just tests
	import matplotlib.pyplot as plt

	osc = SquareOscillator(440.0, 0.5)
	
	cycles = 3
	osc.draw(plt, cycles)
	osc.play()
	plt.show()