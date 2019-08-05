import numpy as np

def integrate(values, interval):
	return (np.cumsum(values) - ((values[0] + values) / 2))*interval

if __name__ == '__main__':

	#the code below is just tests
	import matplotlib.pyplot as plt

	n = 44100
	b = 1.0
	ts = np.linspace(0, b, n + 1)
	#ys = np.sin(ts)
	ys = ts
	#ys = np.ones(ts.shape)
	integrals = integrate(ys, b / n)

	plt.plot(ts, ys, label='values')
	plt.plot(ts, integrals, label='integrals')
	plt.legend()

	plt.show()