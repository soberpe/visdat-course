import matplotlib.pyplot as plt

#plt.plot([1, 2, 3, 4])
#plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
#plt.ylabel('some numbers')
#plt.show()

#plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
#plt.axis((0, 6, 0, 20))
#plt.show()

import numpy as np

# evenly sampled time at 200ms intervals
##t = np.arange(0., 5., 0.2)

# red dashes, blue squares and green triangles
#plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
#plt.show()




#data = {'a': np.arange(50),
        #'c': np.random.randint(0, 50, 50),
        #'d': np.random.randn(50)}
#data['b'] = data['a'] + 10 * np.random.randn(50)
#data['d'] = np.abs(data['d']) * 100

#plt.scatter('a', 'b', c='c', s='d', data=data)
#plt.xlabel('entry a')
#plt.ylabel('entry b')
#plt.show()





# names = ['group_a', 'group_b', 'group_c']
# values = [1, 10, 100]

# plt.figure(figsize=(9, 3))

# plt.subplot(311)
# plt.bar(names, values)
# plt.subplot(312)
# plt.scatter(names, values)
# plt.subplot(313)
# plt.plot(names, values)
# plt.suptitle('Categorical Plotting')
# plt.show()







