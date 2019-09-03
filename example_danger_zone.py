import matplotlib.pyplot as plt

from fm import FMOperator
from mixer import Mixer
from keyboard import MonoKeyboard
from generators import Gate

#basic frequency
freq = 220

#initialize operators
op1 = FMOperator(20.0063*freq, .2)
op2 = FMOperator(1.0003*freq, 1.8)
op3 = FMOperator(1.0003*freq, .59)

op4 = FMOperator(6.9978*freq, .2)
op5 = FMOperator(0.9997*freq, 1.4)
op6 = FMOperator(0.9997*freq, .57)

#set up algorithm

#op1-->op2-->op3--\
#op4-->op5-->op6---\-->mixer-->speaker

op3.add_modulator(op2)
op2.add_modulator(op1)

op6.add_modulator(op5)
op5.add_modulator(op4)

mixer = Mixer()

mixer.add_input(op3)
mixer.add_input(op6)
mixer.set_level(0, 0.125)
mixer.set_level(1, 0.125)


#set up envelopes
op1.set_eg_params(0.0, 0.11, 0.0, 0.05)
op2.set_eg_params(0.0, 0.5, 0.3, 0.2)
op3.set_eg_params(0.0, 0.5, 0.3, 0.4)

op4.set_eg_params(0.0, 0.11, 0.0, 0.05)
op5.set_eg_params(0.0, 0.7, 0.2, 0.2)
op6.set_eg_params(0.0, 0.7, 0.2, 0.4)


#add keyboard
kbd = MonoKeyboard()

ops = [op1, op2, op3, op4, op5, op6]
for op in ops:
	op.set_keyboard(kbd)

#read a midi file
kbd.read_midi('midi\\dangerzonebass.mid')

#draw envelopes, keyboard outputs and the wave shape
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

for op in ops:
	op.eg.draw(ax2, 13, density=2000, alpha=0.5)

kbd.gate.draw(ax2, 13, density=20000, alpha=0.5)
kbd.key.draw(ax3, 13, density=2000)

mixer.draw(ax1, 1.0 / 110, density=1000)

#play the sound
mixer.play(13)

#show the outputs
plt.show()