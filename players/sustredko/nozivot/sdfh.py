from common import *
from utils import *

class OurClient:
    potential = [3970, 1, 0, 0]

i = Vector.normals.index(Vector((1, 0)))
potential = [OurClient.potential[i], OurClient.potential[i-1], OurClient.potential[(i+1)%4]]
najlepsi = (-1, -1)
for i in range(3):
    if dirs[i] >= 1:
        najlepsi = max(najlepsi, (potential[i], i))

print(najlepsi)
