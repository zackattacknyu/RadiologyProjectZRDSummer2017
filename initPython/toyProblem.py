import numpy as np
import matplotlib.pyplot as plt

#compare probability p vs 1-(1-p/2)^2


maxNvalue = 2
pValues = np.linspace(0,1,100)

for NN in range(1,maxNvalue+1):
    innerTerm = pValues * (-1 / NN) + 1
    resultProb = -1 * np.power(innerTerm, NN) + 1
    plt.plot(pValues,resultProb,label='If NumOffers='+str(NN))
plt.xlabel('Probability p')
plt.ylabel('Probability of Sucess')
plt.legend()
plt.show()
