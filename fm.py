import numpy as np
import sounddevice as sd

import constants as const
import math_func as mf

from oscillators import Oscillator, SineOscillator, SquareOscillator
from mixer import Mixer
from triggerables import ADSR
from amplifier import Amplifier
from generators import Gate

class LinearFMGenerator(Oscillator):
	"""A class to represent a sound generator with Linear FM"""

	def __init__(
		self, freq=440.0, level=1.0, phase=0.0, feedback=0, type='sine', 
		mod=None, key_in=None
	):
		#initialize essential parameters
		Oscillator.__init__(self, key_in)

		self.freq = freq
		self.level = level
		self.phase = phase
		self.mod = mod
		self.feedback = feedback

		#initialize operators carrier generator
		if type == 'sine':
			self.carrier = SineOscillator(freq, level, phase, key_in)
		elif type == 'square':
			self.carrier = SquareOscillator(freq, level, phase, key_in)
		#there will be other types in the future

	def set_modulator(self, mod):
		"""Adds a modulator"""
		self.mod = mod

	def set_key_in(self, key_in):
		self.key_in = key_in
		self.carrier.set_key_in(key_in)

	def mod_int(self, t, **kwargs):
		"""
		Returns the integral of values given by self.mod_out(T) for T from 0 to 
		t
		This value is used to generate the modulated signal
		"""

		if self.mod is None:
			return 0.0
		else:
			if type(t) == np.ndarray:
				return mf.integrate(self.mod.output(t, **kwargs), 1.0 / const.fs)
			else:
				if t == 0:
					return 0.0
				else:
					return ((
							self.mod.output(t, **kwargs) + 
							self.mod.output(t - 1.0 / const.fs, **kwargs)
						) / 2*const.fs + 
						self.mod_int(t - (1.0 / const.fs), **kwargs)
					)

	def output(self, t, **kwargs):
		"""Returns the value of operators signal in time t"""
		
		return self.carrier.output(t + self.mod_int(t, **kwargs), **kwargs)

class DXGenerator(LinearFMGenerator):
	"""
	A class to represent a sound generator such as present on the Yamaha DX 
	synthesizer series
	"""

	def output(self, t, **kwargs):
		"""Returns the value of operators signal in time t"""
		
		return self.carrier.output(
			t + self.mod.output(t, **kwargs) / self.freq, 
			**kwargs
		)


class FMOperator(Oscillator):
	"""A class to represent an FM operator"""

	def __init__(
		self, freq=440.0, level=1.0, phase=0.0, feedback=0, wave_type='sine', 
		fm_type='LinearFM', gate=Gate([0.0]), key_in=None
	):
		Oscillator.__init__(self, key_in)

		self.freq = freq

		self.mixer = Mixer()

		if fm_type == 'LinearFM':			
			self.generator = LinearFMGenerator(
				freq, level, phase, feedback, wave_type, self.mixer, key_in
			)
		elif fm_type == 'DX':
			self.generator = DXGenerator(
				freq, level, phase, feedback, wave_type, self.mixer, key_in
			)

		self.eg = ADSR(input=gate)
		self.amp = Amplifier(input=self.generator, mod=self.eg)

	def add_modulator(self, mod, level=1.0):
		"""Adds a modulator"""
		self.mixer.add_input(mod, level)

	def set_key_in(self, key_in):
		"""Sets key input"""
		self.key_in = key_in
		self.generator.set_key_in(key_in)

	def set_eg_params(self, *args, **kwargs):
		"""Sets parameters of the envelope"""
		self.eg.set_params(*args, **kwargs)

	def set_gate(self, gate):
		self.eg.set_input(gate)

	def set_keyboard(self, keyboard):
		"""sets key and gate input from a keybord"""
		self.set_key_in(keyboard.key)
		self.set_gate(keyboard.gate)

	def output(self, t, **kwargs):
		"""Returns the value of operators signal in time t"""
		return self.amp.output(t, **kwargs)

	def draw(self, ax, time=None, cycles=1, **kwargs):
		"""
		Draws the shape of the operators output signal along with its 
		modulators and modulators' modulators etc.
		
		If 'time' is not provided, the shape will be drawn for 'cycles' cycles 
		of operators carrier generator
		"""

		#draw the operators output signal
		Oscillator.draw(self, ax, time, cycles, **kwargs)

		#draw modulators' output signals

		if time is None:
			time = cycles / np.float64(self.freq)

		try:
			kwargs['alpha'] *= 0.5
		except KeyError:
			kwargs['alpha'] = 0.5

		self.mixer.draw(ax, time, **kwargs)


if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	from generators import Ramp, Const
	from keyboard import MonoKey, MonoKeyboard

	freq = 440
	op1 = FMOperator(freq, 0.75, fm_type='DX')
	op2 = FMOperator(freq, 0.45, fm_type='DX')
	op3 = FMOperator(freq, 0.45, fm_type='DX')
	
	op2.add_modulator(op3)
	op1.add_modulator(op2)
	
	#op1.add_modulator(SquareOscillator(op1.freq / 2.0, 0.5))
	#op1.add_modulator(Const(0.5))


	#"""	
	gate = Gate([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
	keyboard = MonoKeyboard(gate=gate, steps=[1,2,3,4], pitches=[12,4,7,0])
	#gate.draw(plt, 8, density=500)

	op1.set_keyboard(keyboard)
	op2.set_keyboard(keyboard)
	op3.set_keyboard(keyboard)
	
	op1.set_eg_params(0.0, 0.5, .5, 1.5)
	op2.set_eg_params(0.0675, 0.5, 0.5, 1.5)
	op3.set_eg_params(0.0675, 0.0675, .125, 0.25)

	"""
	op1.eg.draw(plt, 8, density=500)
	op2.eg.draw(plt, 8, density=500)
	op3.eg.draw(plt, 8, density=500)

	op1.draw(plt, 8, density=8*const.fs)
	"""
	
	op1.draw(plt, cycles=2)
	
	#"""

	"""
	ts = np.linspace(0, cycles / float(op2.freq), 100*cycles)
	ys = op1.freq*op1.mod_int(ts)
	plt.plot(ts, ys, '--', label='op2 integral')

	ys = op2.freq*op2.mod_int(ts)
	plt.plot(ts, ys, '--', label='op3 integral')
	#"""

	op1.play(6)

	plt.show() 