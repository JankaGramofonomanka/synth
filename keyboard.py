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

		self.set_attributes(steps, pitches)

	def set_attributes(self, steps, pitches):
		"""Sets pitches and the points in time when pitches are changed"""

		#'steps' are time points when pitches are changed
		#'pitches' is a sequence of pitches mientioned above

		#'pitches' shouldn't be longer than 'steps'
		if len(steps) < len(pitches):
			pitches = pitches[:len(steps)]

		"""
		we will add 0 at the beginning of 'pitches' and 'steps' and "infinity" 
		(a very big number) at the end of 'steps' for convenience
		"""
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

		self.gate = gate						#gate output
		if steps is None:
			steps = gate.presses

		self.key = MonoKey(steps, pitches)		#key output

	def key_out(self, t, **kwargs):
		"""Returns the key output of the keyboard"""
		return self.key.output(t, **kwargs)

	def gate_out(self, t, **kwargs):
		"""Returns the gate output of the keyboard"""
		return self.gate.output(t, **kwargs)

	def read_midi(self, filename, track=0):
		"""Reads a midi file and converts it to key and gate outputs"""

		tempo = 500000		#default tempo

		#read the file
		mid = mido.MidiFile(filename)

		ts = []				#gate openings and closings

		#we will need those to set up key output
		steps = []
		pitches = []

		pressed = []		#list of pressed keys

		time = 0.0			#this will hold the current time

		for msg in mid.tracks[0]:

			#make 'time' the current time
			#('msg.time' is the time that passed since previous event)
			time += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)

			#change tempo
			if msg.type == 'set_tempo':
				tempo = msg.tempo
				continue

			#ignore anything that doesn' interest you
			elif msg.type != 'note_on':
				continue


			if msg.velocity > 0:
				#'msg.velocity' > 0 means a key was pressed,
				if pressed == []:
					
					"""
					no key is pressed, therefore gate is closed, 
					therefore open the gate
					"""
					ts.append(time)

				#add the key to 'pressed' if it's not there
				if msg.note not in pressed:
					
					pressed.append(msg.note)
				
				#change the pitch
				steps.append(time)
				pitches.append(msg.note - 69)

			else:
				#'msg.velocity' = 0 means a key was released
				if msg.note in pressed:

					#remove the key from 'pressed'
					pressed.remove(msg.note)

					if pressed == []:

						#no key is pressed, therefore close the gate
						ts.append(time)
					else:

						#change the pitch
						steps.append(time)
						pitches.append(msg.note - 69)

		#set up gate and key outputs
		self.gate.set_triggers(ts)
		self.key.set_attributes(steps, pitches)


if __name__ == '__main__':

	#tests
	import matplotlib.pyplot as plt

	from fm import FMOperator

	kbd = MonoKeyboard()
	kbd.read_midi('midi\\wlazkoteknaplotek_mono.mid')

	time = 10

	kbd.gate.draw(plt, time, density=20000)
	kbd.key.draw(plt, time, density=2000)

	freq = 440
	op1 = FMOperator(freq, 0.75, fm_type='DX')
	op2 = FMOperator(freq, 0.75, fm_type='DX')
	op3 = FMOperator(freq, 0.45, fm_type='DX')
	
	op2.add_modulator(op3)
	op1.add_modulator(op2)
	
	op1.set_eg_params(0.01, 0.25, .5, 0.5)
	op2.set_eg_params(0.0675, 0.25, 0.5, 0.5)
	op3.set_eg_params(0.0675, 0.0675, .125, 0.25)

	op1.set_keyboard(kbd)
	op2.set_keyboard(kbd)
	op3.set_keyboard(kbd)

	op1.eg.draw(plt, time, density=2000)
	op2.eg.draw(plt, time, density=2000)
	op3.eg.draw(plt, time, density=2000)

	op1.play(time)

	plt.show()