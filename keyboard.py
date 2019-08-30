import numpy as np
import mido

import constants as const

from generators import Generator, Gate

class MonoKey(Generator):
	"""
	A class to represent a part of a keybord that sends an output signal 
	represeting which key is pressed at a given time
	"""

	def __init__(self, steps=[], pitches=[]):

		if len(steps) < len(pitches):
			pitches = pitches[:len(steps)]

		self.steps = np.full((len(steps) + 2), 0.0)
		self.pitches = np.full((len(pitches) + 1), 0, dtype=np.int32)

		self.steps[0] = 0
		self.steps[1:-1] = steps
		self.steps[-1] = const.inf

		self.pitches[0] = 0.0
		self.pitches[1:] = pitches

	def output(self, t, **kwargs):
		"""Returns the value of generators signal in time t"""
		return np.sum(
			self.pitches[i]*np.int32(
				np.logical_and(self.steps[i] <= t, t < self.steps[i + 1])
			) for i in range(len(self.pitches))
		)

class MonoKeyboard():
	"""A class to represent a monophonic keyboard"""

	def __init__(self, gate=Gate([]), pitches=[], steps=None):

		self.gate = gate
		if steps is None:
			steps = gate.presses

		self.key = MonoKey(steps, pitches)

	def key_out(self, t, **kwargs):
		return self.key.output(t, **kwargs)

	def gate_out(self, t, **kwargs):
		return self.gate.output(t, **kwargs)

	def read_midi(self, filename, track=0):

		tempo = 500000

		mid = mido.MidiFile(filename)

		ts = []
		steps = []
		pitches = []

		pressed = []
		time = 0.0

		for msg in mid.tracks[0]:

			time += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)

			if msg.type == 'set_tempo':
				tempo = msg.tempo
				continue

			elif msg.type != 'note_on':
				continue

			if msg.velocity > 0:
				if pressed == []:
					ts.append(time)

				if msg.note not in pressed:
					
					pressed.append(msg.note)
					
					steps.append(time)
					pitches.append(msg.note - 69)
			else:
				if msg.note in pressed:
					
					pressed.remove(msg.note)

					if pressed == []:
						ts.append(time)
					else:
						steps.append(time)
						pitches.append(msg.note - 69)


		self.gate = Gate(ts)
		self.key = MonoKey(steps, pitches)


if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	from fm import FMOperator

	kbd = MonoKeyboard()
	kbd.read_midi('wlazkoteknaplotek.mid')

	kbd.gate.draw(plt, 20, density=2000)
	kbd.key.draw(plt, 20, density=2000)

	freq = 440
	op1 = FMOperator(freq, 0.75, fm_type='DX')
	op2 = FMOperator(freq, 0.75, fm_type='DX')
	op3 = FMOperator(freq, 0.45, fm_type='DX')
	
	#op2.add_modulator(op3)
	op1.add_modulator(op2)
	
	op1.set_eg_params(0.01, 0.5, .5, 1.5)
	op2.set_eg_params(0.0675, 0.5, 0.5, 1.5)
	op3.set_eg_params(0.0675, 0.0675, .125, 0.25)

	op1.set_keyboard(kbd)
	op2.set_keyboard(kbd)
	op3.set_keyboard(kbd)

	op1.play(20)

	plt.show()