import numpy as np
import sounddevice as sd

from generators import Generator

class Oscillator(Generator):
	"""A class to represent a basic oscillator"""

	def __init__(self, key_in=None):
		self.freq = 440.0 		#generators frequency
		self.key_in = key_in	#keyboard input

	def set_key_in(self, key_in):
		self.key_in = key_in

	def get_key_mod(self, t, ignore_mod=False, **kwargs):
		"""
		Returns the value by which the basic frequency of the oscillator has to 
		be multiplied in time t, due to keyboard input
		"""

		if ignore_mod or self.key_in is None:
			return 1.0
		else:
			return 2**(self.key_in.output(t, **kwargs) / 12)

	def output(self, t, **kwargs):
		"""Returns the value of generators signal in time t"""

		key_mod = self.get_key_mod(t, **kwargs)
		return np.sin(key_mod*self.freq*2*np.pi*t)

	def draw(self, ax, time=None, cycles=1 ,**kwargs):
		"""Draws the signals wave shape"""

		#if time is not provided draw the wave shape 'cycles' times
		if time is None:
			time = cycles / np.float64(self.freq)

			try:
				kwargs['density'] *= cycles
			except KeyError:
				kwargs['density'] = 100*cycles

		Generator.draw(self, ax, time, **kwargs)

class SineOscillator(Oscillator):
	"""A class to represent a sine wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0, key_in=None):

		#initialize essential parameters
		Oscillator.__init__(self, key_in)

		self.freq = freq		#frequency
		self.amp = amp			#amplitude
		self.phase = phase		#phase

	def output(self, t, **kwargs):
		"""Returns the value of oscillators signal in time t"""
		
		key_mod = self.get_key_mod(t, **kwargs)
		return self.amp*np.sin(key_mod*self.freq*2*np.pi*t + self.phase)

class SquareOscillator(Oscillator):
	"""A class to represent a square wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0, pw=0.5, key_in=None):
		
		#initialize essential parameters
		Oscillator.__init__(self, key_in)

		self.freq = freq		#frequency
		self.amp = amp			#amplitude
		self.phase = phase		#phase
		self.pw = pw			#pulse width

	def output(self, t, **kwargs):
		"""Returns the value of oscillators signal in time t"""

		key_mod = self.get_key_mod(t, **kwargs)
		current_phase = (key_mod*self.freq*t + (self.phase / (2*np.pi))) % 1.0

		return self.amp*(2*np.float64(current_phase < self.pw) - 1)

class SawOscillator(Oscillator):
	"""A class to represent a saw wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0, key_in=None):
		
		#initialize essential parameters
		Oscillator.__init__(self, key_in)

		self.freq = freq		#frequency
		self.amp = amp			#amplitude
		self.phase = phase		#phase

	def output(self, t, **kwargs):
		"""Returns the value of oscillators signal in time t"""
		
		key_mod = self.get_key_mod(t, **kwargs)
		return self.amp*(
			-2*((key_mod*self.freq*t + (self.phase / (2*np.pi))) % 1.0) + 1
		)

class RampOscillator(SawOscillator):
	"""A class to represent a ramp (inverse saw) wave oscillator"""

	def output(self, t, **kwargs):
		"""Returns the value of oscillators signal in time t"""
		return -SawOscillator.output(self, t, **kwargs)

class TriangleOscillator(Oscillator):
	"""A class to represent a saw wave oscillator"""

	def __init__(self, freq=440.0, amp=1.0, phase=0.0, pw=0.5, key_in=None):
		
		#initialize essential parameters
		Oscillator.__init__(self, key_in)

		self.freq = freq		#frequency
		self.amp = amp			#amplitude
		self.phase = phase		#phase
		
		"""
		'pw' here means in what phase of the wave's cycle the signal stops 
		ascending and starts descending (0 - at the beginning, 1 - at the end)
		"""
		self.pw = pw

	def output(self, t, **kwargs):
		"""Returns the value of oscillators signal in time t"""

		key_mod = self.get_key_mod(t, **kwargs)
		current_phase = (key_mod*self.freq*t + (self.phase / (2*np.pi))) % 1.0
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

	import constants as const
	from keyboard import MonoKey


	osc = TriangleOscillator(
		220, phase=0.5*np.pi, pw=0.125, 
		key_in=MonoKey(steps=[1,2,3,4], pitches=[12,4,7,0])
		)
	
	osc.draw(plt)
	osc.play(5)
	plt.show() 