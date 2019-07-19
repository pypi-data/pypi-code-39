import numpy as np
from bdfparse import Font
import matplotlib.pyplot as plt

font = Font("9x18.bdf")

plt.imshow(font.word("Hello!"))
plt.show()

