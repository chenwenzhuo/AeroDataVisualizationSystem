import numpy as np
import matplotlib.pyplot as plt


def stream():
    w = 3
    Y, X = np.mgrid[-w:w:100j, -w:w:100j]
    U = -1 - X ** 2 + Y
    V = 1 + X - Y ** 2

    plt.streamplot(X, Y, U, V, density=[0.5, 1])
    print(U)
    print("-----------------------")
    print(Y)

    plt.show()


if __name__ == '__main__':
    stream()
