import numpy as np
import sounddevice as sd

import math_func as mf
from oscillators import Oscillator, SineOscillator, SquareOscillator

class FMOperator(Oscillator):
	"""A class to represent an FM operator"""

	def __init__(
		self, freq=440.0, level=1.0, phase=0.0, feedback=0, type='sine'
	):
		#initialize essential parameters
		self.freq = freq
		self.level = level
		self.phase = phase
		self.modulators = []
		self.feedback = feedback

		#initialize operators carrier generator
		if type == 'sine':
			self.generator = SineOscillator(freq, level, phase)
		elif type == 'square':
			self.generator = SquareOscillator(freq, level, phase)
		#there will be other types in the future

	def add_modulator(self, mod):
		"""Adds a modulator"""
		self.modulators.append(mod)

	def mod_out(self, t):
		"""Returns the sum ofthe values of all modulators at time t"""
		if self.modulators == []:
			return 0.0
		else:
			return np.sum(mod.output(t) for mod in self.modulators)

	def mod_int(self, t):
		"""
		Returns the integral of values given by self.mod_out(T) for T from 0 to 
		t
		This value is used to generate the modulated signal
		"""

		if self.modulators == []:
			return 0.0
		else:
			if type(t) == np.ndarray:
				return mf.integrate(self.mod_out(t), 1.0 / self.fs)
			else:
				if t == 0:
					return 0.0
				else:
					return (
						(self.mod_out(t) + self.mod_out(t - (1.0 / self.fs))) 
						/ 2*self.fs + self.mod_int(t - (1.0 / self.fs))
					)

	def output(self, t):
		"""Returns the value of operators signal in time t"""
		
		mod = self.mod_int(t)
		return self.generator.output(t + mod)

	def draw(self, ax, time=None, density=100, alpha=1.0, scale=1.0, cycles=1):
		"""
		Draws the shape of the operators output signal along with its 
		modulators and modulators' modulators etc.
		
		The shape will be drawn for 'cycles' cycles of operators carrier 
		generator
		"""
		if time is None:
			time = cycles / float(self.freq)
			density = density*cycles

		#draw the operators output signal
		Oscillator.draw(self, ax, time, density, alpha)

		#draw modulators' output signals
		for mod in self.modulators:
			mod.draw(ax, time, density, 0.5*alpha)


if __name__ == '__main__':

	#the code below is just tests
	import matplotlib.pyplot as plt

	op1 = FMOperator(440, 0.75)
	#osc = SineOscillator(440.0, 1.0)
	op2 = FMOperator(440.0, 1.0)
	op3 = FMOperator(440.0, 1.0)
	#op4 = FMOperator(32*440.0, 0.5)
	
	#op3.add_modulator(op4)
	op2.add_modulator(op3)
	op1.add_modulator(op2)

	#"""
	cycles = 4
	op1.draw(plt, cycles=cycles)

	ts = np.linspace(0, cycles / float(op2.freq), 100*cycles)
	ys = op1.freq*op1.mod_int(ts)
	plt.plot(ts, ys, '--', label='op2 integral')

	ys = op2.freq*op2.mod_int(ts)
	plt.plot(ts, ys, '--', label='op3 integral')

	op1.play(2)

	plt.legend()
	plt.show() 