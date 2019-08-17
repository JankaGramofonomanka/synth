import numpy as np

import constants as const
import math_func as mf
from generators import Generator, Gate

class Triggerable(Generator):
	"""A mother class to represent all triggerable modules"""

	def __init__(self, input=Gate(), threshold=0.5):

		self.input = input
		self.threshold = threshold

	def set_input(self, input):
		"""Sets an input of the generator"""
		self.input = input

	def get_presses(self, ts):
		"""Returns an array of times when gate was opened (key was pressed)"""
		
		if type(self.input) == Gate:
			return self.input.presses

		else:
			output = self.input.output(ts)
			offset = np.full(output.shape, 0.0)
			offset[1:] = output[:-1]

			indices = np.logical_and(
				output > self.threshold, offset <= self.threshold
			)
			return ts[indices]

	def get_releases(self, ts):
		"""Returns an array of times when gate was closed (key was released)"""


		if type(self.input) == Gate:
			return self.input.releases

		else:
			output = self.input.output(ts)
			offset = np.full(output.shape, 0.0)
			offset[1:] = output[:-1]

			indices = np.logical_and(
				output < self.threshold, offset >= self.threshold
			)
			return ts[indices]	

	def before_release(self, t):
		"""
		Returns the output signal given that the gate is opened at time 0, and 
		never closed
		"""

		if type(t) == np.ndarray:
			return np.ones(t.shape, dtype=np.float64)
		else:
			return 1.0


	def after_release(self, t):
		"""
		Returns the output signal given that the gate is opened and immediately 
		closed at time 0
		"""

		if type(t) == np.ndarray:
			return np.zeros(t.shape, dtype=np.float64)
		else:
			return 0.0

	def output(self, t):
		
		if type(t) == np.ndarray:
			#return self.before_release(t) 
			presses = self.get_presses(t)
			releases = self.get_releases(t)
			n = presses.shape[0]

			output = np.zeros(t.shape)

			i = 0
			press = presses[i]
			while True:
				
				try:
					release = releases[i]
				except IndexError:
					release = const.inf
				
				output += (
					self.before_release(t - press)
					*np.float64(np.logical_and(press <= t, t < release))
				)

				prev_press = press
				
				try:
					press = presses[i + 1]
				except IndexError:
					press = const.inf

				output += (
					self.before_release(release - prev_press)
					*self.after_release(t - release)
					*np.float64(np.logical_and(release <= t, t < press))
				)

				if press >= const.inf:
					break

				i += 1

			return output
		
		else:
			#This will be implemented in the future, I hope
			return 0.0

class ADSR(Triggerable):
	"""A class to represent an envelope generator of ADSR type"""

	def __init__(
		self, attack=0.0, decay=0.0, sustain=1.0, release=0.0, 
		input=Gate(), threshold=0.5
	):
		Triggerable.__init__(self, input, threshold)

		self.attack = attack
		self.decay = decay
		self.sustain = sustain
		self.release = release

	def set_params(self, attack, decay, sustain, release):

		self.attack = attack
		self.decay = decay
		self.sustain = sustain
		self.release = release

	def before_release(self, t):
		"""
		Returns the output signal given that the gate is opened at time 0, and 
		never closed
		"""

		attack = (
			mf.line((0, 0), (self.attack, 1.0), t)
			*np.float64(np.logical_and(t >= 0, t < self.attack))
		)
		decay = (
			mf.line(
				(self.attack, 1.0), (self.attack + self.decay, self.sustain), t
			)
			*np.float64(
				np.logical_and(t >= self.attack, t < self.attack + self.decay)
			)
		)
		sustain = self.sustain*np.float64(t >= self.attack + self.decay)
		
		return attack + decay + sustain

	def after_release(self, t):
		"""
		Returns the output signal given that the gate is opened and immediately 
		closed at time 0
		"""
		return (
			mf.line((0, 1), (self.release, 0), t)*np.float64(t < self.release)
		)

if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	from oscillators import SineOscillator
	from amplifier import Amplifier


	input = Gate([1,2,3,5,5.25, 8])
	eg = ADSR(input=input)
	time = 10.0

	eg.draw(plt, time, density=5*44100)

	eg.set_params(0.25, 0.25, 0.25, 0.25)
	eg.draw(plt, time, density=5*44100)

	eg.set_params(0.5, 0.5, 0.75, 0.75)
	eg.draw(plt, time, density=5*44100)

	eg.set_params(0.75, 0.75, 0.75, 1.75)
	eg.draw(plt, time, density=5*44100)

	plt.show()