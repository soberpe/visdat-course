import matplotlib.pyplot as plt
import numpy as np

x1=np.linspace(0, 10, 100)
y1=np.log(x1)
x2=np.cos(x1)
y2=np.sin(y1)


# plt.plot(x, y, linewidth=6.0)
# line, = plt.plot(x1, y1, x2, y2, '-')
# line.set_antialiased(False) # turn off antialiasing
# plt.show()

lines = plt.plot(x1, y1, x2, y2)
# use keyword arguments
plt.setp(lines, color='r', linewidth=2.0)
# or MATLAB style string value pairs
plt.setp(lines, 'color', 'r', 'linewidth', 2.0)
plt.show()