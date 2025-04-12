import numpy as np

def heuristic(X1,X2,Y1,Y2):
    
    return np.sqrt((X1 - X2) ** 2 + (Y1 - Y2) ** 2)


print(heuristic(2,6,2,3))
print(heuristic(2,5,2,6))
