import numpy as np

def integrate(values, interval):
	return (np.cumsum(values) - ((values[0] + values) / 2))*interval

def line(A, B, x):
	a = (A[1] - B[1]) / (A[0] - B[0])
	b = A[1] - a*A[0]
	return a*x + b


if __name__ == '__main__':

	#the code below is just tests
	import matplotlib.pyplot as plt

	bottom = -1
	top = 2
	left = -1
	right = 2

	plt.ylim(bottom, top)

	for i in range(bottom, top + 1):	
		plt.plot([left, right], [i, i], alpha=0.2, color='k')
	for i in range(left, right + 1):	
		plt.plot([i, i], [bottom, top], alpha=0.2, color='k')
	
	b = (1.1, 0)
	a = (1, 1)

	plt.scatter([a[0], b[0]], [a[1], b[1]])

	xs = np.linspace(left, right, 100)
	ys = line(a, b, xs)
	plt.plot(xs, ys)
	plt.show()