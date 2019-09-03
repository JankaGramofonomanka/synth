I Requirements:

This project uses python 3.7 and the following libraries:

	numpy
	matplotlib
	sounddevice
	mido



II Desription and usage:

This project is a collection of classes that represent various modules that can 
be used to create a synthesizer

All elementary modules ('subclasses of 'Generator, currently there is only one non-elementary module - 'MonoKeyboard') have 'output' 'draw' and 'play' methods.

Let 'module' be a name of an elementary module. 

'module.output(t)' will return the value of the signal generated or processed 
by 'module' in time 't' (in seconds). If 't' is a numpy array, it will also 
return a numpy array of 'module's signal values (not all modules will accept 
't' as a number, all however accept numpy arrays).

'module.draw(ax, time)' will draw the values 'Module.output(t)' from 't' = 0 to 
't' = 'time', given that 'ax' is set to 'matplotlib.pyplot' or its subplot.

'module.play(t)' will play the sound generated or processed by 'Module' for 't' 
seconds.

Note: all elementary modules have the 'play' method, however some are 
designed to generate modulating signal instead of sound, therefore when the 
'play' method will be called no sound will be heard.



To create a synthesizer, one must connect different modules. This can be done 
by setting one module's output as another's input. There are several types of 
input:

1. The first type is an input that will be processed by a module, eg. an input 
of an amplifier or a mixer.

2. Key input - it as an attribute of all subclasses of 'Oscillator', that is 
modules designed to generate sound (as opposed to modulators). It's purpose is 
to "tell" the module which key is pressed on a keyboard so that the module will 
adjust its frequency accordingly. An increase of the input's value by 1 
corresponds to the increase by 1 semitone on the keyboard, the value 0 
corresponds to the key A1. 
(The attribute is called 'key_in')

3.Gate input - this input is used to "tell" a module when a key is pressed on 
a keyboard. by default the value 1 means that a key is pressed, 0 that it 
isn't. 

Other inputs can be used to modulate frequency, amplitude, etc.

All inputs are attributes of modules and instances of other elementary module 
classes.
Usually you can connect modules in the following fashion:
	module1.input1 = module2
Some modules are more complicated and you will have to look for a method that 
will set an input for you (the method will be named with a prefix 'set_' or 
'add_'). Then it will look like this:
	module1.set_input1(module2)
Some modules can have inputs assigned to them by a constructor:
	module1 = Module(*args, input1=module2)
For details you will have to look into the source code.



The non-elementary modules are different becouse they have no 'output' method. 
And that is because they generate more then one output. A Keyboard for instance 
has to generate key and gate outputs, somtimes also velocity, therefore A class 
representing a keyboard will have attributes that will be instances of 
elementary modules, each generating a different output. These attributes can be 
connected to other modules just like any other non-input modules.